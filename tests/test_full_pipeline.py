#!/usr/bin/env python3
"""
完整的爬虫端到端测试
验证整个流程：登录 → 搜索 → 提取 → 分析
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scrapers.spider import XhsSpider, FishSpider

async def test_full_pipeline():
    """测试完整的爬虫流程"""
    print("=" * 80)
    print("🔥 小红书爬虫 - 完整端到端测试")
    print("=" * 80)
    
    spider = XhsSpider()
    
    try:
        # 初始化
        print("\n1️⃣  初始化爬虫...")
        await spider.init_browser()
        print("   ✅ 爬虫已初始化")
        
        # 检查登录
        print("\n2️⃣  检查登录状态...")
        is_logged = await spider.check_login_status()
        if not is_logged:
            print("   ❌ 未登录！")
            return False
        print("   ✅ 已登录")
        
        # 执行爬取
        print("\n3️⃣  执行爬取任务...")
        keywords = ["复古相机"]  # 测试单一关键词
        
        results = await spider.get_xhs_trends(keywords)
        
        print("\n4️⃣  爬取结果：")
        for keyword, data in results.items():
            print(f"\n   关键词: {keyword}")
            print(f"   数据源: {data.get('source', 'unknown')}")
            print(f"   笔记数: {data.get('count', 0)}")
            print(f"   趋势分: {data.get('trend_score', 0)}")
            
            notes = data.get('notes', [])
            if notes:
                print(f"   前3条笔记:")
                for i, note in enumerate(notes[:3], 1):
                    print(f"     {i}. {note.get('title', 'N/A')[:50]}")
                    print(f"        用户: {note.get('user', 'N/A')}")
                    print(f"        点赞: {note.get('likes', 0)}")
        
        print("\n✅ 测试完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        print("\n清理资源...")
        await spider.close()

async def main():
    success = await test_full_pipeline()
    
    if success:
        print("\n" + "=" * 80)
        print("✅ 完整流程测试成功!")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("❌ 完整流程测试失败!")
        print("=" * 80)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
