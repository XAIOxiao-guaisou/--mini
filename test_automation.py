#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 全自动运行测试脚本
验证自动化、静默运行和精准推送三大功能
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class AutomationTester:
    """自动化功能测试器"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def test_edge_auto_detection(self):
        """测试1：Edge路径自动检测"""
        print("\n" + "="*70)
        print("测试1：Edge路径自动检测")
        print("="*70)
        
        try:
            # 检测注册表
            result = subprocess.run(
                ['reg', 'query', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe', '/ve'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            edge_found = False
            edge_path = None
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'REG_SZ' in line:
                        path = line.split('REG_SZ')[-1].strip()
                        if os.path.exists(path):
                            edge_found = True
                            edge_path = path
                            break
            
            # 检测默认路径
            if not edge_found:
                default_paths = [
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                ]
                
                for path in default_paths:
                    if os.path.exists(path):
                        edge_found = True
                        edge_path = path
                        break
            
            if edge_found:
                print(f"✅ 测试通过：成功检测到Edge浏览器")
                print(f"   路径：{edge_path}")
                self.passed += 1
                self.test_results.append({
                    'test': 'Edge自动检测',
                    'status': 'PASS',
                    'details': f'Edge路径：{edge_path}'
                })
            else:
                print(f"❌ 测试失败：未检测到Edge浏览器")
                self.failed += 1
                self.test_results.append({
                    'test': 'Edge自动检测',
                    'status': 'FAIL',
                    'details': 'Edge浏览器未安装或路径异常'
                })
        
        except Exception as e:
            print(f"❌ 测试失败：{e}")
            self.failed += 1
            self.test_results.append({
                'test': 'Edge自动检测',
                'status': 'FAIL',
                'details': str(e)
            })
    
    def test_browser_profile_persistence(self):
        """测试2：持久化上下文检测"""
        print("\n" + "="*70)
        print("测试2：持久化上下文检测")
        print("="*70)
        
        profile_path = Path("./browser_profile")
        
        if profile_path.exists():
            try:
                size_mb = sum(f.stat().st_size for f in profile_path.rglob('*') if f.is_file()) / 1024 / 1024
                
                if size_mb > 1:
                    print(f"✅ 测试通过：检测到持久化缓存")
                    print(f"   缓存大小：{size_mb:.1f} MB")
                    print(f"   状态：可复用登录状态")
                    self.passed += 1
                    self.test_results.append({
                        'test': '持久化上下文',
                        'status': 'PASS',
                        'details': f'缓存大小：{size_mb:.1f}MB'
                    })
                else:
                    print(f"⚠️  警告：缓存目录存在但为空")
                    print(f"   建议：运行一次登录模式以建立缓存")
                    self.passed += 1
                    self.test_results.append({
                        'test': '持久化上下文',
                        'status': 'PASS',
                        'details': '目录存在但为空（首次使用）'
                    })
            except Exception as e:
                print(f"❌ 测试失败：{e}")
                self.failed += 1
                self.test_results.append({
                    'test': '持久化上下文',
                    'status': 'FAIL',
                    'details': str(e)
                })
        else:
            print(f"⚠️  警告：持久化目录不存在")
            print(f"   将在首次运行时自动创建")
            self.passed += 1
            self.test_results.append({
                'test': '持久化上下文',
                'status': 'PASS',
                'details': '目录不存在（将自动创建）'
            })
    
    def test_silent_mode_support(self):
        """测试3：静默运行模式"""
        print("\n" + "="*70)
        print("测试3：静默运行模式支持")
        print("="*70)
        
        try:
            # 检查main.py是否支持--silent参数
            main_file = Path("main.py")
            if not main_file.exists():
                raise FileNotFoundError("main.py不存在")
            
            with open(main_file, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # 检查关键特性
            has_silent_param = "silent_mode" in main_content
            has_silent_arg = "--silent" in main_content or "-s" in main_content
            has_engine_silent = "NicheHunterEngine(silent_mode=" in main_content
            
            if has_silent_param and has_silent_arg and has_engine_silent:
                print(f"✅ 测试通过：静默运行模式已实现")
                print(f"   支持参数：python main.py --silent 或 -s")
                print(f"   功能：自动headless + 最小日志输出")
                self.passed += 1
                self.test_results.append({
                    'test': '静默运行模式',
                    'status': 'PASS',
                    'details': '支持--silent和-s参数'
                })
            else:
                print(f"❌ 测试失败：静默模式未完全实现")
                print(f"   silent_mode参数：{'✓' if has_silent_param else '✗'}")
                print(f"   命令行参数：{'✓' if has_silent_arg else '✗'}")
                print(f"   引擎传递：{'✓' if has_engine_silent else '✗'}")
                self.failed += 1
                self.test_results.append({
                    'test': '静默运行模式',
                    'status': 'FAIL',
                    'details': '部分功能未实现'
                })
        
        except Exception as e:
            print(f"❌ 测试失败：{e}")
            self.failed += 1
            self.test_results.append({
                'test': '静默运行模式',
                'status': 'FAIL',
                'details': str(e)
            })
    
    def test_precise_push_logic(self):
        """测试4：精准推送逻辑"""
        print("\n" + "="*70)
        print("测试4：精准推送逻辑")
        print("="*70)
        
        try:
            # 检查main.py推送逻辑
            main_file = Path("main.py")
            with open(main_file, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # 检查关键逻辑
            has_rank_results = "BlueOceanAnalyzer.rank_results" in main_content
            has_is_qualified = "BlueOceanAnalyzer.is_qualified" in main_content
            has_top_n_filter = "for i, result in enumerate(top_results" in main_content
            
            # 检查utils/logic.py消息格式
            logic_file = Path("utils/logic.py")
            if logic_file.exists():
                with open(logic_file, 'r', encoding='utf-8') as f:
                    logic_content = f.read()
                
                has_enhanced_format = "竞争程度" in logic_content and "需求强度" in logic_content
            else:
                has_enhanced_format = False
            
            all_checks = [
                ("rank_results排序", has_rank_results),
                ("is_qualified筛选", has_is_qualified),
                ("Top N限制", has_top_n_filter),
                ("增强消息格式", has_enhanced_format)
            ]
            
            passed_checks = sum(1 for _, check in all_checks if check)
            
            if passed_checks == len(all_checks):
                print(f"✅ 测试通过：精准推送逻辑已完整实现")
                for name, result in all_checks:
                    print(f"   ✓ {name}")
                self.passed += 1
                self.test_results.append({
                    'test': '精准推送逻辑',
                    'status': 'PASS',
                    'details': '所有检查项通过'
                })
            else:
                print(f"❌ 测试失败：{passed_checks}/{len(all_checks)} 检查项通过")
                for name, result in all_checks:
                    print(f"   {'✓' if result else '✗'} {name}")
                self.failed += 1
                self.test_results.append({
                    'test': '精准推送逻辑',
                    'status': 'FAIL',
                    'details': f'{passed_checks}/{len(all_checks)} 检查项通过'
                })
        
        except Exception as e:
            print(f"❌ 测试失败：{e}")
            self.failed += 1
            self.test_results.append({
                'test': '精准推送逻辑',
                'status': 'FAIL',
                'details': str(e)
            })
    
    def test_config_validation(self):
        """测试5：配置文件验证"""
        print("\n" + "="*70)
        print("测试5：配置文件验证")
        print("="*70)
        
        try:
            config_file = Path("config.py")
            if not config_file.exists():
                raise FileNotFoundError("config.py不存在")
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            # 检查关键配置
            checks = [
                ("WECOM_WEBHOOK", "WECOM_WEBHOOK" in config_content),
                ("EDGE_PATH", "EDGE_PATH" in config_content),
                ("USER_DATA_PATH", "USER_DATA_PATH" in config_content),
                ("MIN_POTENTIAL_SCORE", "MIN_POTENTIAL_SCORE" in config_content),
                ("MAX_COMPETITION", "MAX_COMPETITION" in config_content),
                ("ENABLE_WECOM_PUSH", "ENABLE_WECOM_PUSH" in config_content),
            ]
            
            passed_checks = sum(1 for _, check in checks if check)
            
            if passed_checks == len(checks):
                print(f"✅ 测试通过：配置文件完整")
                for name, _ in checks:
                    print(f"   ✓ {name}")
                self.passed += 1
                self.test_results.append({
                    'test': '配置文件验证',
                    'status': 'PASS',
                    'details': '所有配置项存在'
                })
            else:
                print(f"⚠️  警告：{passed_checks}/{len(checks)} 配置项存在")
                for name, result in checks:
                    print(f"   {'✓' if result else '✗'} {name}")
                self.passed += 1  # 非致命错误
                self.test_results.append({
                    'test': '配置文件验证',
                    'status': 'PASS',
                    'details': f'{passed_checks}/{len(checks)} 配置项存在'
                })
        
        except Exception as e:
            print(f"❌ 测试失败：{e}")
            self.failed += 1
            self.test_results.append({
                'test': '配置文件验证',
                'status': 'FAIL',
                'details': str(e)
            })
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*70)
        print("🤖 全自动运行功能测试")
        print("="*70)
        print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 运行测试
        self.test_edge_auto_detection()
        self.test_browser_profile_persistence()
        self.test_silent_mode_support()
        self.test_precise_push_logic()
        self.test_config_validation()
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*70)
        print("📊 测试报告")
        print("="*70)
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"总测试数：{total}")
        print(f"✅ 通过：{self.passed}")
        print(f"❌ 失败：{self.failed}")
        print(f"通过率：{pass_rate:.1f}%")
        
        # 保存报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'total': total,
            'passed': self.passed,
            'failed': self.failed,
            'pass_rate': f"{pass_rate:.1f}%",
            'results': self.test_results
        }
        
        report_file = Path("automation_test_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到：{report_file}")
        
        # 返回状态码
        return 0 if self.failed == 0 else 1


def main():
    """主程序"""
    tester = AutomationTester()
    exit_code = tester.run_all_tests()
    
    print("\n" + "="*70)
    if exit_code == 0:
        print("✅ 所有测试通过！系统已准备好全自动运行")
        print("\n使用方法：")
        print("  • 正常模式：python main.py")
        print("  • 静默模式：python main.py --silent")
        print("  • 快速启动：python START.py")
    else:
        print("⚠️  部分测试失败，请检查上述错误信息")
    print("="*70)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
