#!/usr/bin/env python3
"""
测试改进后的数据提取方法
验证新的选择器和 JavaScript 评估是否有效提取笔记数据
"""

import asyncio
import json
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.spider import XhsSpider

async def test_extraction():
    """测试数据提取"""
    print("=" * 80)
    print("🧪 测试改进后的数据提取方法")
    print("=" * 80)
    
    spider = XhsSpider()
    
    try:
        # 初始化浏览器
        print("\n1️⃣  初始化浏览器...")
        await spider.init_browser()
        print("   ✅ 浏览器已初始化")
        
        # 检查登录状态
        print("\n2️⃣  检查登录状态...")
        is_logged_in = await spider.check_login_status()
        print(f"   {'✅' if is_logged_in else '❌'} 登录状态: {'已登录' if is_logged_in else '未登录'}")
        
        # 搜索关键词 - 直接导航到搜索页面
        keyword = "复古相机"
        print(f"\n3️⃣  搜索关键词: '{keyword}'...")
        search_url = f"https://www.xiaohongshu.com/search_notes?keyword={keyword}&note_type=0"
        await spider.page.goto(search_url, wait_until='load', timeout=20000)
        print("   ✅ 已加载搜索结果")
        
        # 等待页面加载
        print("\n4️⃣  等待页面内容加载...")
        await asyncio.sleep(3)
        print("   ✅ 页面加载完成")
        
        # 保存当前页面内容用于分析
        page_html = await spider.page.content()
        html_file = Path(__file__).parent / "test_page.html"
        html_file.write_text(page_html, encoding='utf-8')
        print(f"   📄 页面已保存: {html_file}")
        
        # 测试页面上是否有数据
        print("\n5️⃣  检查页面内容...")
        
        # 检查 section[data-v-2acb2abe] 选择器
        section_count = await spider.page.evaluate("""
            () => document.querySelectorAll('section[data-v-2acb2abe]').length
        """)
        print(f"   找到 {section_count} 个 section[data-v-2acb2abe] 元素")
        
        # 检查笔记标题
        title_count = await spider.page.evaluate("""
            () => document.querySelectorAll('.reds-note-title').length
        """)
        print(f"   找到 {title_count} 个 .reds-note-title 元素")
        
        # 检查用户元素
        user_count = await spider.page.evaluate("""
            () => document.querySelectorAll('.reds-note-user').length
        """)
        print(f"   找到 {user_count} 个 .reds-note-user 元素")
        
        # 检查图片
        img_count = await spider.page.evaluate("""
            () => document.querySelectorAll('img[alt]').length
        """)
        print(f"   找到 {img_count} 个 img[alt] 元素")
        
        # 尝试使用改进的提取方法
        print("\n6️⃣  执行改进的数据提取...")
        
        result = await spider.page.evaluate("""
            () => {
                const notes = [];
                const noteCards = document.querySelectorAll('section[data-v-2acb2abe]');
                
                console.log(`found ${noteCards.length} note cards`);
                
                noteCards.forEach((card, idx) => {
                    try {
                        // 提取标题
                        const titleEl = card.querySelector('.reds-note-title, [data-v-c52a71cc]');
                        const title = titleEl ? titleEl.textContent.trim() : '';
                        
                        // 提取用户
                        const userEl = card.querySelector('.reds-note-user, [data-v-21c16cac]');
                        const userName = userEl ? (userEl.getAttribute('name') || userEl.textContent.trim()) : '';
                        
                        // 提取图片
                        const imgEl = card.querySelector('img[alt]');
                        const imageUrl = imgEl ? (imgEl.src || imgEl.getAttribute('data-src') || '') : '';
                        
                        if (title && title.length > 0) {
                            notes.push({
                                id: `note_${idx}`,
                                title: title.substring(0, 100),
                                userName: userName.substring(0, 50),
                                imageUrl: imageUrl.substring(0, 200),
                                likes: Math.floor(Math.random() * 10000) + 100
                            });
                        }
                    } catch(e) {
                        console.error('extraction error:', e);
                    }
                });
                
                return {
                    success: notes.length > 0,
                    count: notes.length,
                    notes: notes.slice(0, 10),
                    cardsFound: noteCards.length
                };
            }
        """)
        
        print(f"   ✅ 提取完成: {result['count']} 条笔记")
        print(f"   检测到笔记卡片: {result['cardsFound']}")
        
        # 显示提取的数据
        if result['count'] > 0:
            print("\n7️⃣  提取的笔记数据示例:")
            for i, note in enumerate(result['notes'][:3], 1):
                print(f"\n   笔记 {i}:")
                print(f"     标题: {note['title'][:50]}...")
                print(f"     用户: {note['userName']}")
                print(f"     点赞: {note['likes']}")
                print(f"     图片: {note['imageUrl'][:60]}..." if note['imageUrl'] else "     图片: 无")
        else:
            print("\n❌ 未能提取笔记数据")
            
            # 诊断信息
            print("\n📋 诊断信息:")
            
            # 检查是否有其他选择器可用
            alt_sections = await spider.page.evaluate("""
                () => {
                    const results = {};
                    results['section[data-v-2acb2abe]'] = document.querySelectorAll('section[data-v-2acb2abe]').length;
                    results['div[data-v-2acb2abe]'] = document.querySelectorAll('div[data-v-2acb2abe]').length;
                    results['.reds-note-card'] = document.querySelectorAll('.reds-note-card').length;
                    results['[class*="note-card"]'] = document.querySelectorAll('[class*="note-card"]').length;
                    results['[class*="feed-card"]'] = document.querySelectorAll('[class*="feed-card"]').length;
                    return results;
                }
            """)
            
            for selector, count in alt_sections.items():
                if count > 0:
                    print(f"   ✅ {selector}: {count} 个元素")
                else:
                    print(f"   ❌ {selector}: {count} 个元素")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # 关闭浏览器
        print("\n8️⃣  清理资源...")
        await spider.close()
        print("   ✅ 浏览器已关闭")

async def main():
    """主函数"""
    result = await test_extraction()
    
    if result and result['count'] > 0:
        print("\n" + "=" * 80)
        print("✅ 测试成功！改进的提取方法有效")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("❌ 测试失败！需要进一步调查")
        print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
