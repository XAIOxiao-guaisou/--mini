"""
蓝海赛道分析模块（Enhanced版本）
分析小红书热度和闲鱼商品数据，找出最具潜力的投入方向
"""

import json
import logging
from typing import List, Dict, Tuple
from datetime import datetime

from config import (
    XHS_DATA_FILE, FISH_DATA_FILE, REPORT_FILE,
    MAX_COMPETITION, MIN_POTENTIAL_SCORE, TOP_N_RESULTS,
    ENABLE_WECOM_PUSH
)
from engine.analyzer import BlueOceanAnalyzer
from utils.logic import NichePushLogic


# 日志配置
logger = logging.getLogger(__name__)


class NicheFinder:
    """蓝海赛道发现器（离线版本）"""
    
    def __init__(self, xhs_file: str = XHS_DATA_FILE, fish_file: str = FISH_DATA_FILE):
        """
        初始化分析器
        
        Args:
            xhs_file: 小红书数据文件路径
            fish_file: 闲鱼数据文件路径
        """
        self.xhs_file = xhs_file
        self.fish_file = fish_file
        self.xhs_data = {}
        self.fish_data = {}
        self.notifier = NichePushLogic() if ENABLE_WECOM_PUSH else None
        
    def load_data(self) -> bool:
        """
        加载数据文件
        
        Returns:
            是否加载成功
        """
        success = True
        
        try:
            with open(self.xhs_file, 'r', encoding='utf-8') as f:
                self.xhs_data = json.load(f)
            print(f"✓ 已加载小红书数据：{len(self.xhs_data)} 个词条")
            logger.info(f"加载小红书数据成功：{len(self.xhs_data)} 个词条")
        except FileNotFoundError:
            print(f"⚠ 警告：未找到文件 {self.xhs_file}")
            logger.warning(f"文件不存在：{self.xhs_file}")
            self.xhs_data = {}
            success = False
        except json.JSONDecodeError as e:
            print(f"✗ 错误：{self.xhs_file} 格式错误 - {e}")
            logger.error(f"JSON解析错误：{e}")
            self.xhs_data = {}
            success = False
            
        try:
            with open(self.fish_file, 'r', encoding='utf-8') as f:
                self.fish_data = json.load(f)
            print(f"✓ 已加载闲鱼数据：{len(self.fish_data)} 个词条")
            logger.info(f"加载闲鱼数据成功：{len(self.fish_data)} 个词条")
        except FileNotFoundError:
            print(f"⚠ 警告：未找到文件 {self.fish_file}")
            logger.warning(f"文件不存在：{self.fish_file}")
            self.fish_data = {}
            success = False
        except json.JSONDecodeError as e:
            print(f"✗ 错误：{self.fish_file} 格式错误 - {e}")
            logger.error(f"JSON解析错误：{e}")
            self.fish_data = {}
            success = False
        
        return success
    
    def analyze(self, max_fish_count: int = MAX_COMPETITION, top_n: int = TOP_N_RESULTS) -> List[Dict]:
        """
        执行蓝海分析
        
        Args:
            max_fish_count: 闲鱼商品数上限（超过此值视为竞争过于激烈）
            top_n: 返回前 N 个最佳赛道
            
        Returns:
            潜力赛道列表
        """
        results = []
        
        # 获取所有词条（取并集）
        all_keywords = set(self.xhs_data.keys()) | set(self.fish_data.keys())
        
        print(f"\n正在分析 {len(all_keywords)} 个词条...\n")
        
        for keyword in all_keywords:
            # 获取小红书数据
            xhs_info = self.xhs_data.get(keyword, {})
            xhs_heat = xhs_info.get('热度', 0) if isinstance(xhs_info, dict) else 0
            
            # 获取闲鱼数据
            fish_info = self.fish_data.get(keyword, {})
            fish_count = fish_info.get('商品数', 0) if isinstance(fish_info, dict) else 0
            
            # 过滤：剔除商品数超过上限的词条
            if fish_count > max_fish_count:
                continue
            
            # 计算蓝海指数
            index, info = BlueOceanAnalyzer.calculate_detailed_index(
                xhs_data={'word': keyword, 'heat': xhs_heat},
                fish_data=fish_info if isinstance(fish_info, dict) else {'商品数': 0, '平均想要': 0}
            )
            
            # 只保留有效数据
            if index > 0:
                results.append(info)
        
        # 排序和筛选
        results = BlueOceanAnalyzer.rank_results(results, top_n)
        
        return results
    
    def print_report(self, results: List[Dict]) -> None:
        """
        打印分析报告
        
        Args:
            results: 分析结果列表
        """
        print("\n" + "="*80)
        print("🎯 蓝海赛道分析报告")
        print("="*80)
        
        if not results:
            print("\n⚠ 暂无符合条件的赛道数据")
            return
        
        for i, item in enumerate(results, 1):
            print(f"\n【第 {i} 名】{item['词条']}")
            print(f"  🔥 蓝海指数：{item['蓝海指数']:,.2f} {item['评级']}")
            print(f"  📊 数据详情：")
            print(f"     • 小红书热度：{item['小红书热度']:,.0f} {item['热度评估']}")
            print(f"     • 闲鱼商品数：{item['闲鱼商品数']} {item['竞争度评估']}")
            print(f"     • 闲鱼想要总数：{item.get('闲鱼想要数', [])}")
            print(f"     • 平均想要人数：{item['平均想要数']:.2f}")
        
        print("\n" + "="*80)
        print("分析完成 ✓")
        print("="*80 + "\n")
    
    def save_report(self, results: List[Dict], output_file: str = REPORT_FILE) -> None:
        """
        保存分析报告为 JSON 文件
        
        Args:
            results: 分析结果列表
            output_file: 输出文件路径
        """
        report = {
            '生成时间': datetime.now().isoformat(),
            '分析规则': {
                '蓝海指数计算': '(小红书热度 × 平均想要人数) / (闲鱼商品数 + 1)',
                '过滤条件': f'闲鱼商品数 ≤ {MAX_COMPETITION}',
                '推送阈值': f'蓝海指数 ≥ {MIN_POTENTIAL_SCORE}',
                '排序依据': '蓝海指数降序'
            },
            '潜力赛道': []
        }
        
        for i, item in enumerate(results, 1):
            report['潜力赛道'].append({
                '排名': i,
                '词条': item['词条'],
                '蓝海指数': item['蓝海指数'],
                '评级': item['评级'],
                '数据详情': {
                    '小红书热度': item['小红书热度'],
                    '闲鱼商品数': item['闲鱼商品数'],
                    '闲鱼想要数': item.get('闲鱼想要数', []),
                    '平均想要人数': item['平均想要数']
                },
                '评估': {
                    '热度评估': item['热度评估'],
                    '竞争度评估': item['竞争度评估']
                }
            })
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✓ 报告已保存至：{output_file}")
            logger.info(f"报告已保存：{output_file}")
        except Exception as e:
            print(f"✗ 保存报告失败：{e}")
            logger.error(f"保存报告异常：{e}")
    
    def push_results(self, results: List[Dict]) -> int:
        """
        推送符合条件的结果到企业微信
        
        Args:
            results: 分析结果列表
            
        Returns:
            成功推送的个数
        """
        if not self.notifier or not results:
            return 0
        
        # 过滤符合推送条件的结果
        qualified = [
            r for r in results
            if r['蓝海指数'] >= MIN_POTENTIAL_SCORE 
            and r['闲鱼商品数'] <= MAX_COMPETITION
        ]
        
        if not qualified:
            print(f"⚠ 没有符合推送条件的赛道（蓝海指数 ≥ {MIN_POTENTIAL_SCORE}）")
            return 0
        
        print(f"\n📤 准备推送 {len(qualified)} 个优质赛道到企业微信...")
        return self.notifier.batch_push(qualified)
    
    def run(self, max_fish_count: int = MAX_COMPETITION, top_n: int = TOP_N_RESULTS, 
            save_json: bool = True, output_file: str = REPORT_FILE,
            push_to_wecom: bool = ENABLE_WECOM_PUSH) -> List[Dict]:
        """
        运行完整分析流程
        
        Args:
            max_fish_count: 闲鱼商品数上限
            top_n: 返回前 N 个最佳赛道
            save_json: 是否保存 JSON 报告
            output_file: JSON 报告文件名
            push_to_wecom: 是否推送到企业微信
            
        Returns:
            分析结果列表
        """
        print("🚀 启动蓝海赛道离线分析...\n")
        print(f"📋 配置信息：")
        print(f"   • 竞争度阈值：≤ {max_fish_count} 个商品")
        print(f"   • 蓝海指数阈值：≥ {MIN_POTENTIAL_SCORE}")
        print(f"   • 返回结果数：前 {top_n} 名")
        print(f"   • 企业微信推送：{'开启' if push_to_wecom else '关闭'}\n")
        
        # 1. 加载数据
        if not self.load_data():
            print("⚠ 数据加载失败，部分功能可能受影响")
        
        # 2. 执行分析
        results = self.analyze(max_fish_count=max_fish_count, top_n=top_n)
        
        # 3. 打印报告
        self.print_report(results)
        
        # 4. 保存报告
        if save_json and results:
            self.save_report(results, output_file)
        
        # 5. 推送到企业微信
        if push_to_wecom and results:
            self.push_results(results)
        
        return results


def main():
    """主函数：演示模块使用"""
    # 创建分析器实例（使用配置文件中的默认值）
    finder = NicheFinder()
    
    # 运行分析（使用配置文件中的阈值）
    results = finder.run(
        max_fish_count=MAX_COMPETITION,
        top_n=TOP_N_RESULTS,
        save_json=True,
        output_file=REPORT_FILE,
        push_to_wecom=ENABLE_WECOM_PUSH
    )
    
    return results


if __name__ == '__main__':
    main()
