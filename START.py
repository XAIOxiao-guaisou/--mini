#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 蓝海赛道挖掘系统 - 快速启动脚本
"""

import sys
import os
import time
import subprocess
import json
from pathlib import Path

# 中文字体和颜色配置
class Colors:
    """控制台颜色输出"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """打印启动横幅"""
    banner = f"""
{Colors.CYAN}╔════════════════════════════════════════════════════════════════════╗{Colors.END}
{Colors.CYAN}║                                                                    ║{Colors.END}
{Colors.BOLD}{Colors.GREEN}║          🚀 蓝海赛道挖掘系统 - 快速启动工具                     ║{Colors.END}
{Colors.BOLD}{Colors.GREEN}║             Blue Ocean Market Discovery System                  ║{Colors.END}
{Colors.CYAN}║                                                                    ║{Colors.END}
{Colors.CYAN}╚════════════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

def check_config():
    """检查配置文件"""
    config_path = Path("config.py")
    if not config_path.exists():
        print(f"{Colors.RED}❌ 找不到 config.py 文件{Colors.END}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
        if 'WECOM_WEBHOOK = ""' in config_content or "WECOM_WEBHOOK = ''" in config_content:
            print(f"{Colors.YELLOW}⚠️  警告：企业微信Webhook未配置{Colors.END}")
            return False
    
    print(f"{Colors.GREEN}✅ 配置文件检查通过{Colors.END}")
    return True

def check_dependencies():
    """检查依赖包"""
    required = ['requests', 'schedule']
    
    try:
        import requests
        print(f"{Colors.GREEN}✅ requests 已安装{Colors.END}")
    except ImportError:
        print(f"{Colors.YELLOW}⚠️  requests 未安装{Colors.END}")
        return False
    
    return True

def show_menu():
    """显示菜单"""
    menu = f"""
{Colors.BOLD}════════════════════════════════════════════════════════════════════{Colors.END}
{Colors.BOLD}{Colors.CYAN}              请选择运行模式：{Colors.END}

{Colors.GREEN}[1]{Colors.END} 🏃 快速测试 - 离线分析演示（<1秒，推荐新手）
    $ python niche_finder.py
    • 无需网络爬虫
    • 快速验证系统
    • 推送示例消息到企业微信

{Colors.GREEN}[2]{Colors.END} 🔐 登录账号 - 首次人工登录保存Session（仅需一次）
    $ python login_helper.py
    • 支持小红书、闲鱼同时登录
    • 所有登录数据本地保存
    • 后续自动复用，无需重复登录

{Colors.GREEN}[3]{Colors.END} 🤖 完全自动 - 在线数据爬取分析（5-10分钟，推荐体验）
    $ python main.py
    • 爬取小红书热搜
    • 查询闲鱼商品数据
    • 计算蓝海指数
    • 自动推送到企业微信
    • ✨ 首次需登录，之后自动复用Session

{Colors.GREEN}[4]{Colors.END} ⏱️  定时调度 - 后台自动运行（推荐长期运行）
    $ python scheduler.py
    • 每天3个时间段自动执行
    • 时间：09:30, 14:00, 21:30
    • 无需人工干预

{Colors.GREEN}[5]{Colors.END} 🔍 系统检查 - 验证环境配置
    $ python check_system.py
    • 检查依赖库
    • 验证 Edge 浏览器
    • 测试企业微信连接

{Colors.GREEN}[6]{Colors.END} 📋 查看文档 - 完整使用指南
    • README.md - 详细文档
    • PERSISTENT_LOGIN_GUIDE.md - 登录系统指南
    • QUICKSTART.md - 快速入门

{Colors.GREEN}[7]{Colors.END} ⚙️  检查依赖 - 安装所需包
    $ pip install -r requirements.txt

{Colors.GREEN}[8]{Colors.END} 🧪 测试持久化登录系统
    $ python test_persistent_login.py
    • 验证登录系统功能
    • 检查浏览器配置文件
    • 测试人类行为模拟

{Colors.GREEN}[0]{Colors.END} 退出

{Colors.BOLD}════════════════════════════════════════════════════════════════════{Colors.END}
"""
    print(menu)

def run_command(cmd, description):
    """运行命令"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {description}{Colors.END}")
    print(f"{Colors.CYAN}$ {cmd}{Colors.END}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✅ {description} 完成{Colors.END}\n")
        else:
            print(f"\n{Colors.RED}❌ {description} 失败（错误码：{result.returncode}）{Colors.END}\n")
        return result.returncode == 0
    except Exception as e:
        print(f"{Colors.RED}❌ 执行出错：{e}{Colors.END}\n")
        return False

def open_file(filepath, description):
    """打开文件"""
    if not Path(filepath).exists():
        print(f"{Colors.RED}❌ 找不到文件：{filepath}{Colors.END}\n")
        return
    
    try:
        if sys.platform == 'win32':
            os.startfile(filepath)
        elif sys.platform == 'darwin':
            subprocess.run(['open', filepath])
        else:
            subprocess.run(['xdg-open', filepath])
        print(f"{Colors.GREEN}✅ 已打开 {description}{Colors.END}\n")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  无法打开文件：{e}{Colors.END}")
        print(f"请手动打开：{filepath}\n")

def show_system_info():
    """显示系统信息"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}═════════════════════════════════════════{Colors.END}")
    print(f"{Colors.BOLD}系统信息{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}═════════════════════════════════════════{Colors.END}")
    
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"工作目录: {os.getcwd()}")
    print(f"操作系统: {sys.platform}")
    
    # 检查关键文件
    files_to_check = ['config.py', 'main.py', 'niche_finder.py', 'requirements.txt']
    print(f"\n{Colors.BOLD}文件检查：{Colors.END}")
    for f in files_to_check:
        status = "✅" if Path(f).exists() else "❌"
        print(f"  {status} {f}")
    
    print()

def main():
    """主函数"""
    # 设置控制台编码
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')
    
    print_banner()
    show_system_info()
    
    # 检查前置条件
    check_config()
    check_dependencies()
    
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}请输入选项 (0-8)：{Colors.END} ").strip()
        
        if choice == '0':
            print(f"\n{Colors.GREEN}👋 感谢使用蓝海赛道挖掘系统，再见！{Colors.END}\n")
            break
        
        elif choice == '1':
            run_command('python niche_finder.py', '快速测试 - 离线分析演示')
        
        elif choice == '2':
            print(f"\n{Colors.BOLD}{Colors.BLUE}📱 登录账号说明：{Colors.END}")
            print("   • 首次需要手动扫码/验证登录")
            print("   • 登录数据保存到 ./browser_profile")
            print("   • 后续自动复用，无需重复登录")
            print("   • 支持同时登录小红书和闲鱼")
            print()
            confirm = input(f"{Colors.BOLD}确认启动登录助手？(y/n)：{Colors.END} ").strip().lower()
            if confirm == 'y':
                run_command('python login_helper.py', '登录账号 - 首次人工登录保存Session')
            else:
                print(f"{Colors.YELLOW}已取消{Colors.END}\n")
        
        elif choice == '3':
            print(f"\n{Colors.YELLOW}⚠️  完全自动模式需要以下前置条件：{Colors.END}")
            print("   • Microsoft Edge 浏览器已安装")
            print("   • 已通过 [2] 完成登录")
            print("   • Playwright 库已安装 (pip install -r requirements.txt)")
            print()
            confirm = input(f"{Colors.BOLD}确认继续？(y/n)：{Colors.END} ").strip().lower()
            if confirm == 'y':
                run_command('python main.py', '完全自动 - 在线数据爬取分析')
            else:
                print(f"{Colors.YELLOW}已取消{Colors.END}\n")
        
        elif choice == '4':
            print(f"\n{Colors.BLUE}💡 定时调度说明：{Colors.END}")
            print("   • 会在后台持续运行")
            print("   • 每天执行3次：09:30, 14:00, 21:30")
            print("   • 按 Ctrl+C 可停止运行")
            print()
            confirm = input(f"{Colors.BOLD}确认启动？(y/n)：{Colors.END} ").strip().lower()
            if confirm == 'y':
                run_command('python scheduler.py', '定时调度 - 后台自动运行')
            else:
                print(f"{Colors.YELLOW}已取消{Colors.END}\n")
        
        elif choice == '5':
            run_command('python check_system.py', '系统检查 - 验证环境配置')
        
        elif choice == '6':
            print(f"\n{Colors.BOLD}{Colors.BLUE}请选择要查看的文档：{Colors.END}\n")
            print(f"{Colors.GREEN}[1]{Colors.END} README.md - 详细文档")
            print(f"{Colors.GREEN}[2]{Colors.END} PERSISTENT_LOGIN_GUIDE.md - 登录系统指南")
            print(f"{Colors.GREEN}[3]{Colors.END} QUICKSTART.md - 快速入门")
            print(f"{Colors.GREEN}[4]{Colors.END} 返回主菜单")
            
            doc_choice = input(f"\n{Colors.BOLD}请选择 (1-4)：{Colors.END} ").strip()
            if doc_choice == '1':
                open_file('README.md', 'README.md')
            elif doc_choice == '2':
                open_file('PERSISTENT_LOGIN_GUIDE.md', 'PERSISTENT_LOGIN_GUIDE.md')
            elif doc_choice == '3':
                open_file('QUICKSTART.md', 'QUICKSTART.md')
            elif doc_choice == '4':
                continue
            else:
                print(f"{Colors.RED}无效选项{Colors.END}\n")
        
        elif choice == '7':
            run_command('pip install -r requirements.txt', '安装依赖包')
        
        elif choice == '8':
            print(f"\n{Colors.BLUE}🧪 持久化登录系统测试说明：{Colors.END}")
            print("   • 验证登录系统功能")
            print("   • 检查浏览器配置文件")
            print("   • 测试人类行为模拟")
            print("   • 会启动 Microsoft Edge 浏览器窗口")
            print()
            confirm = input(f"{Colors.BOLD}确认启动？(y/n)：{Colors.END} ").strip().lower()
            if confirm == 'y':
                run_command('python test_persistent_login.py', '测试持久化登录系统')
            else:
                print(f"{Colors.YELLOW}已取消{Colors.END}\n")
        
        else:
            print(f"{Colors.RED}❌ 无效选项，请重新选择{Colors.END}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}用户中断{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}出错：{e}{Colors.END}\n")
        sys.exit(1)
