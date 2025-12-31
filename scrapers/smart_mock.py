"""
🎯 智能Mock数据生成器
基于关键词生成高质量的模拟数据，确保100%数据产出

特性：
- 关键词相关性分析
- 真实数据分布模拟
- 趋势评分智能计算
- 多维度数据生成

作者：iostoupin Team
日期：2025-12-31
"""

import random
import hashlib
from typing import Dict, List
from datetime import datetime, timedelta


class SmartMockGenerator:
    """智能Mock数据生成器"""
    
    # 真实小红书笔记标题模板
    TITLE_TEMPLATES = [
        "{keyword}｜真的太好用了！强烈推荐⭐️",
        "亲测有效！{keyword}使用心得分享💖",
        "{keyword}避坑指南🚫你一定要看！",
        "2025最新{keyword}推荐清单📝",
        "{keyword}保姆级教程来啦✨",
        "宝藏{keyword}！人人都说好👍",
        "{keyword}新手入门必看🔰",
        "终于找到完美的{keyword}了🎉",
        "{keyword}好物分享｜每日一推",
        "我的{keyword}使用日记📖",
    ]
    
    # 用户昵称模板
    NICKNAME_TEMPLATES = [
        "小红薯{id}", "时尚达人{id}", "生活记录者{id}",
        "美好日常{id}", "爱分享的{name}", "种草博主{id}",
        "精致girl{id}", "实用主义者{id}", "好物推荐官{id}"
    ]
    
    # 随机名字池
    NAMES = ["小月", "小雪", "小鱼", "小兔", "小熊", "小猫", "小鸟", "小花"]
    
    def __init__(self):
        """初始化生成器"""
        random.seed()
    
    def generate_notes(self, keyword: str, count: int = 10) -> List[Dict]:
        """
        生成笔记列表
        
        Args:
            keyword: 关键词
            count: 数量
        
        Returns:
            笔记列表
        """
        notes = []
        
        for i in range(count):
            # 生成唯一ID（基于关键词和索引）
            note_id = self._generate_id(keyword, i)
            
            # 选择标题模板
            title_template = random.choice(self.TITLE_TEMPLATES)
            title = title_template.format(keyword=keyword)
            
            # 生成用户名
            nickname = self._generate_nickname(note_id)
            
            # 生成点赞数（符合真实分布：大部分较少，少数爆款）
            likes = self._generate_realistic_likes()
            
            # 生成收藏数（约为点赞的30-50%）
            collects = int(likes * random.uniform(0.3, 0.5))
            
            # 生成评论数（约为点赞的5-15%）
            comments = int(likes * random.uniform(0.05, 0.15))
            
            # 生成发布时间（最近30天内）
            publish_time = self._generate_recent_time()
            
            notes.append({
                "id": note_id,
                "title": title,
                "user": nickname,
                "likes": likes,
                "collects": collects,
                "comments": comments,
                "publish_time": publish_time,
                "type": "视频" if random.random() > 0.6 else "图文",
                "is_mock": True
            })
        
        return notes
    
    def calculate_trend_score(self, notes: List[Dict]) -> int:
        """
        计算趋势分数
        
        Args:
            notes: 笔记列表
        
        Returns:
            趋势分数（0-10000）
        """
        if not notes:
            return 0
        
        # 计算平均互动数
        avg_likes = sum(n["likes"] for n in notes) / len(notes)
        avg_collects = sum(n["collects"] for n in notes) / len(notes)
        avg_comments = sum(n["comments"] for n in notes) / len(notes)
        
        # 权重计算
        trend_score = int(
            avg_likes * 0.5 + 
            avg_collects * 0.3 + 
            avg_comments * 0.2
        )
        
        # 限制范围
        return min(max(trend_score, 100), 10000)
    
    def _generate_id(self, keyword: str, index: int) -> str:
        """生成唯一ID"""
        seed = f"{keyword}_{index}_{datetime.now().strftime('%Y%m%d')}"
        return hashlib.md5(seed.encode()).hexdigest()[:16]
    
    def _generate_nickname(self, note_id: str) -> str:
        """生成用户昵称"""
        # 使用ID的哈希值作为随机种子
        seed = int(note_id[:8], 16)
        random.seed(seed)
        
        template = random.choice(self.NICKNAME_TEMPLATES)
        
        if "{name}" in template:
            name = random.choice(self.NAMES)
            return template.format(name=name)
        else:
            id_suffix = str(seed % 10000).zfill(4)
            return template.format(id=id_suffix)
    
    def _generate_realistic_likes(self) -> int:
        """生成符合真实分布的点赞数"""
        # 80%的笔记点赞数较少（100-1000）
        # 15%的笔记点赞数中等（1000-5000）
        # 5%的笔记是爆款（5000-50000）
        
        rand = random.random()
        
        if rand < 0.80:
            # 普通笔记
            return random.randint(100, 1000)
        elif rand < 0.95:
            # 中等热度
            return random.randint(1000, 5000)
        else:
            # 爆款
            return random.randint(5000, 50000)
    
    def _generate_recent_time(self) -> str:
        """生成最近30天内的随机时间"""
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        time_delta = timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        publish_time = datetime.now() - time_delta
        
        return publish_time.strftime("%Y-%m-%d %H:%M")


# ========================================
# 便捷函数
# ========================================

def quick_generate_mock_data(keyword: str, count: int = 10) -> Dict:
    """
    快速生成Mock数据
    
    Args:
        keyword: 关键词
        count: 笔记数量
    
    Returns:
        完整的数据字典
    
    示例:
        data = quick_generate_mock_data("露营装备", 10)
        print(f"趋势分数: {data['trend_score']}")
    """
    generator = SmartMockGenerator()
    notes = generator.generate_notes(keyword, count)
    trend_score = generator.calculate_trend_score(notes)
    
    return {
        "count": len(notes),
        "trend_score": trend_score,
        "notes": notes,
        "source": "smart_mock",
        "keyword": keyword,
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # 测试
    generator = SmartMockGenerator()
    
    print("="*60)
    print("🎯 智能Mock数据生成器测试")
    print("="*60)
    
    test_keywords = ["露营装备", "咖啡机推荐", "健身器材"]
    
    for keyword in test_keywords:
        data = quick_generate_mock_data(keyword, 5)
        print(f"\n关键词: {keyword}")
        print(f"笔记数: {data['count']}")
        print(f"趋势分数: {data['trend_score']}")
        print(f"示例笔记: {data['notes'][0]['title']}")
        print(f"  点赞: {data['notes'][0]['likes']}, 用户: {data['notes'][0]['user']}")
    
    print("\n" + "="*60)
    print("✅ 测试完成")
