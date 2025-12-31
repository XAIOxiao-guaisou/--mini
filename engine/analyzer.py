"""
蓝海指数分析引擎
实现蓝海指数计算算法：Index = (XHS_Heat × Average_Wants) / (Competition_Count + 1)
"""

from typing import Dict, Tuple
from config import MIN_POTENTIAL_SCORE, MAX_COMPETITION


class BlueOceanAnalyzer:
    """蓝海指数分析器"""
    
    @staticmethod
    def calculate_index(
        xhs_heat: float,
        competition_count: int,
        average_wants: float = 0,
        wants_list: list = None
    ) -> float:
        """
        计算蓝海指数
        
        蓝海指数公式：
        $$Index = \\frac{XHS\_Heat \\times Average\_Wants}{Competition\_Count + 1}$$
        
        其中：
        - XHS_Heat: 小红书笔记互动增长率（热度值）
        - Average_Wants: 闲鱼搜索结果前5名的平均"想要"人数
        - Competition_Count: 闲鱼同标题商品总数
        
        Args:
            xhs_heat: 小红书热度值
            competition_count: 闲鱼竞争对手数
            average_wants: 闲鱼平均想要数（优先使用此参数）
            wants_list: 想要数列表（如提供，则自动计算平均值）
            
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
        
        # 应用蓝海指数公式
        # 分母加1是为了避免竞争数为0时的除零错误，同时惩罚竞争激烈的市场
        index = (xhs_heat * average_wants) / (competition_count + 1)
        
        return round(index, 2)
    
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
