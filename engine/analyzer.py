"""
🧠 蓝海指数分析引擎（v2.0 - 时间衰减进化版）
实现蓝海指数计算算法：Index = (XHS_Heat × Average_Wants) / (Competition_Count + 1) × Time_Decay

核心升级：
- 引入时间衰减系数：24小时内新热搜 × 1.5倍权重加成
- 支持时间戳分析：从xhs_data.json提取发布时间
- 动态调整：热点越新，权重越高

更新日志：
- 2025-12-31: 实现时间衰减系数机制
"""

from typing import Dict, Tuple
from config import MIN_POTENTIAL_SCORE, MAX_COMPETITION
from datetime import datetime, timedelta
import json
import os


class BlueOceanAnalyzer:
    """蓝海指数分析器（时间衰减增强版）"""
    
    @staticmethod
    def _calculate_time_decay_factor(timestamp: str = None, data_file: str = "xhs_data.json") -> float:
        """
        计算时间衰减系数
        
        规则：
        - 24小时内：1.5倍加成
        - 24-48小时：1.3倍加成
        - 48-72小时：1.1倍加成
        - 72小时以上：1.0倍（无加成）
        
        Args:
            timestamp: 数据时间戳（ISO格式）
            data_file: 数据文件路径（自动提取时间）
        
        Returns:
            时间衰减系数（1.0-1.5）
        """
        try:
            # 1. 如果提供了时间戳，直接使用
            if timestamp:
                data_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            # 2. 否则尝试从文件读取
            elif os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 查找时间戳字段
                    if isinstance(data, dict):
                        timestamp_str = data.get('timestamp') or data.get('crawl_time') or data.get('update_time')
                        if timestamp_str:
                            data_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            # 使用文件修改时间
                            file_mtime = os.path.getmtime(data_file)
                            data_time = datetime.fromtimestamp(file_mtime)
                    else:
                        # 使用文件修改时间
                        file_mtime = os.path.getmtime(data_file)
                        data_time = datetime.fromtimestamp(file_mtime)
            else:
                # 无法获取时间，返回默认值
                return 1.0
            
            # 计算时间差
            now = datetime.now()
            time_diff = now - data_time
            hours_ago = time_diff.total_seconds() / 3600
            
            # 应用衰减规则
            if hours_ago <= 24:
                return 1.5  # 24小时内：1.5倍热点加成
            elif hours_ago <= 48:
                return 1.3  # 24-48小时：1.3倍加成
            elif hours_ago <= 72:
                return 1.1  # 48-72小时：1.1倍加成
            else:
                return 1.0  # 72小时以上：无加成
        
        except Exception as e:
            print(f"⚠️ 时间衰减计算失败: {e}，使用默认系数1.0")
            return 1.0
    
    @staticmethod
    def calculate_index(
        xhs_heat: float,
        competition_count: int,
        average_wants: float = 0,
        wants_list: list = None,
        timestamp: str = None,
        enable_time_decay: bool = True
    ) -> float:
        """
        计算蓝海指数（时间衰减增强版）
        
        蓝海指数公式：
        $$Index = \\frac{XHS\_Heat \\times Average\_Wants}{Competition\_Count + 1} \\times Time\_Decay$$
        
        其中：
        - XHS_Heat: 小红书笔记互动增长率（热度值）
        - Average_Wants: 闲鱼搜索结果前5名的平均"想要"人数
        - Competition_Count: 闲鱼同标题商品总数
        - Time_Decay: 时间衰减系数（24h内 × 1.5）
        
        Args:
            xhs_heat: 小红书热度值
            competition_count: 闲鱼竞争对手数
            average_wants: 闲鱼平均想要数（优先使用此参数）
            wants_list: 想要数列表（如提供，则自动计算平均值）
            timestamp: 数据时间戳（用于计算衰减系数）
            enable_time_decay: 是否启用时间衰减（默认启用）
            
        Returns:
            蓝海指数（float）
        """
        
        # 参数验证与修正
        if xhs_heat < 0:
            xhs_heat = 0
        if competition_count < 0:
            competition_count = 0
        
        # 如果提供了列表，自动计算平均值
        if wants_list and len(wants_list) > 0:
            average_wants = sum(wants_list) / len(wants_list)
        
        if average_wants < 0:
            average_wants = 0
        
        # 计算时间衰减系数
        time_decay = 1.0
        if enable_time_decay:
            time_decay = BlueOceanAnalyzer._calculate_time_decay_factor(timestamp)
        
        # 应用增强版蓝海指数公式
        # 分母加1是为了避免竞争数为0时的除零错误，同时惩罚竞争激烈的市场
        base_index = (xhs_heat * average_wants) / (competition_count + 1)
        
        # 应用时间衰减系数
        final_index = base_index * time_decay
        
        # 如果应用了时间加成，输出提示
        if time_decay > 1.0:
            print(f"  ⏰ 时间加成: {time_decay}× (24小时内热点)")
        
        return round(final_index, 2)
    
    @staticmethod
    def calculate_detailed_index(xhs_data: Dict, fish_data: Dict) -> Tuple[float, Dict]:
        """
        计算详细的蓝海指数及分析信息
        
        Args:
            xhs_data: {'word': '词条', 'heat': 热度值}
            fish_data: {'keyword': '词条', '商品数': 数, '平均想要': 数, '想要数列表': []}
            
        Returns:
            (蓝海指数, 详细分析信息字典)
        """
        keyword = xhs_data.get('word', fish_data.get('keyword', 'Unknown'))
        xhs_heat = float(xhs_data.get('heat', 0))
        competition_count = int(fish_data.get('商品数', 0))
        average_wants = float(fish_data.get('平均想要', 0))
        wants_list = fish_data.get('想要数列表', [])
        
        # 计算蓝海指数
        index = BlueOceanAnalyzer.calculate_index(
            xhs_heat=xhs_heat,
            competition_count=competition_count,
            average_wants=average_wants,
            wants_list=wants_list
        )
        
        # 生成分析信息
        analysis = {
            '词条': keyword,
            '小红书热度': xhs_heat,
            '闲鱼商品数': competition_count,
            '闲鱼想要数': wants_list,
            '平均想要数': round(average_wants, 2),
            '蓝海指数': index,
            '评级': BlueOceanAnalyzer.get_rating(index),
            '竞争度评估': BlueOceanAnalyzer.assess_competition(competition_count),
            '热度评估': BlueOceanAnalyzer.assess_heat(xhs_heat)
        }
        
        return index, analysis
    
    @staticmethod
    def get_rating(index: float) -> str:
        """
        根据蓝海指数给出评级
        
        Args:
            index: 蓝海指数
            
        Returns:
            评级文本
        """
        if index >= 1000:
            return "⭐⭐⭐⭐⭐ 顶级蓝海"
        elif index >= 500:
            return "⭐⭐⭐⭐ 优质蓝海"
        elif index >= 200:
            return "⭐⭐⭐ 良好蓝海"
        elif index >= 100:
            return "⭐⭐ 一般蓝海"
        elif index >= MIN_POTENTIAL_SCORE:
            return "⭐ 潜在蓝海"
        else:
            return "❌ 不推荐"
    
    @staticmethod
    def assess_competition(count: int) -> str:
        """
        评估竞争程度
        
        Args:
            count: 竞争对手数
            
        Returns:
            竞争评估文本
        """
        if count <= 50:
            return "✓ 竞争极小"
        elif count <= 100:
            return "✓ 竞争较小"
        elif count <= 200:
            return "△ 竞争适中"
        elif count <= MAX_COMPETITION:
            return "△ 竞争较大"
        else:
            return "✗ 竞争激烈（红海市场）"
    
    @staticmethod
    def assess_heat(heat: float) -> str:
        """
        评估热度程度
        
        Args:
            heat: 小红书热度值
            
        Returns:
            热度评估文本
        """
        if heat >= 50000:
            return "🔥🔥🔥 超高热度"
        elif heat >= 20000:
            return "🔥🔥 很高热度"
        elif heat >= 10000:
            return "🔥 高热度"
        elif heat >= 5000:
            return "△ 中等热度"
        elif heat >= 1000:
            return "⚠ 低热度"
        else:
            return "❌ 极低热度"
    
    @staticmethod
    def is_qualified(index: float, competition: int) -> bool:
        """
        判断词条是否符合推送条件
        
        规则：
        1. 蓝海指数 >= MIN_POTENTIAL_SCORE
        2. 竞争数 <= MAX_COMPETITION
        
        Args:
            index: 蓝海指数
            competition: 竞争对手数
            
        Returns:
            是否符合条件
        """
        return index >= MIN_POTENTIAL_SCORE and competition <= MAX_COMPETITION
    
    @staticmethod
    def rank_results(results: list, top_n: int = 5) -> list:
        """
        对分析结果进行排序和筛选
        
        Args:
            results: 分析结果列表
            top_n: 返回前N个
            
        Returns:
            排序后的前N个结果
        """
        # 按蓝海指数降序排序
        sorted_results = sorted(
            results,
            key=lambda x: x['蓝海指数'],
            reverse=True
        )
        
        # 返回前N个
        return sorted_results[:top_n]


def calculate_index(xhs_heat: float, competition_count: int, average_wants: float) -> float:
    """便捷函数：计算蓝海指数"""
    return BlueOceanAnalyzer.calculate_index(xhs_heat, competition_count, average_wants)


if __name__ == '__main__':
    # 测试蓝海指数计算
    print("="*60)
    print("蓝海指数计算测试")
    print("="*60)
    
    test_cases = [
        {'xhs_heat': 15000, 'competition': 80, 'avg_wants': 15.0},  # 顶级蓝海
        {'xhs_heat': 12000, 'competition': 150, 'avg_wants': 6.0},  # 优质蓝海
        {'xhs_heat': 8000, 'competition': 250, 'avg_wants': 4.0},   # 一般蓝海
        {'xhs_heat': 5000, 'competition': 500, 'avg_wants': 3.0},   # 红海市场
    ]
    
    for i, case in enumerate(test_cases, 1):
        index = calculate_index(
            xhs_heat=case['xhs_heat'],
            competition_count=case['competition'],
            average_wants=case['avg_wants']
        )
        
        rating = BlueOceanAnalyzer.get_rating(index)
        competition_assess = BlueOceanAnalyzer.assess_competition(case['competition'])
        heat_assess = BlueOceanAnalyzer.assess_heat(case['xhs_heat'])
        qualified = BlueOceanAnalyzer.is_qualified(index, case['competition'])
        
        print(f"\n测试用例 {i}：")
        print(f"  小红书热度：{case['xhs_heat']}")
        print(f"  竞争对手数：{case['competition']}")
        print(f"  平均想要数：{case['avg_wants']}")
        print(f"  蓝海指数：{index}")
        print(f"  评级：{rating}")
        print(f"  热度评估：{heat_assess}")
        print(f"  竞争评估：{competition_assess}")
        print(f"  是否推送：{'✓ 是' if qualified else '✗ 否'}")
