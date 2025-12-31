"""
🧪 持久化登录系统测试脚本
验证launch_persistent_context和登录状态检查功能

测试项目：
1. ✅ 持久化上下文启动
2. ✅ Stealth反检测注入
3. ✅ 登录状态检查
4. ✅ 人类行为模拟
5. ✅ 浏览器配置文件保存
"""

import asyncio
import os
from scrapers.spider import XhsSpider, FishSpider
from config import USER_DATA_PATH


async def test_persistent_login():
    """测试持久化登录系统"""
    print("=" * 70)
    print("🧪 持久化登录系统测试")
    print("=" * 70)
    
    # 测试1: 检查用户数据目录
    print("\n【测试1】检查用户数据目录")
    print(f"配置路径: {USER_DATA_PATH}")
    if os.path.exists(USER_DATA_PATH):
        print(f"✅ 目录已存在")
        files = os.listdir(USER_DATA_PATH)
        print(f"📁 包含文件/文件夹: {len(files)} 个")
        if len(files) > 0:
            print(f"   示例: {files[:3]}")
            print("💡 提示: 检测到浏览器配置文件，可能已有登录状态")
        else:
            print("⚠️  目录为空，这是首次运行")
    else:
        print(f"⚠️  目录不存在，将在启动时自动创建")
    
    # 测试2: 小红书爬虫
    print("\n" + "=" * 70)
    print("【测试2】小红书爬虫 - 持久化模式")
    print("=" * 70)
    
    xhs_spider = None
    try:
        xhs_spider = XhsSpider(headless=False, use_stealth=True)
        print("⏳ 启动小红书爬虫...")
        await xhs_spider.init_browser()
        
        print("\n✅ 浏览器启动成功")
        print(f"   - Context类型: {type(xhs_spider.context).__name__}")
        print(f"   - Page类型: {type(xhs_spider.page).__name__}")
        
        # 检查登录状态
        print("\n⏳ 检查登录状态...")
        is_logged_in = await xhs_spider.check_login_status()
        
        if is_logged_in:
            print("✅ 小红书已登录！")
        else:
            print("❌ 小红书未登录")
            print("💡 请运行: python login_helper.py")
        
        # 测试人类行为模拟
        print("\n⏳ 测试人类行为模拟...")
        print("   - 模拟延迟...")
        await xhs_spider.human_delay(1.0, 2.0)
        print("   ✅ 延迟完成")
        
        print("   - 模拟鼠标移动...")
        await xhs_spider.human_mouse_move(400, 300)
        print("   ✅ 鼠标移动完成")
        
        print("   - 模拟滚动...")
        await xhs_spider.human_scroll(200)
        print("   ✅ 滚动完成")
        
        # 保持浏览器打开5秒以便观察
        print("\n⏳ 浏览器窗口将保持5秒...")
        await asyncio.sleep(5)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if xhs_spider:
            await xhs_spider.close()
            print("\n✅ 小红书爬虫已关闭")
    
    # 测试3: 闲鱼爬虫
    print("\n" + "=" * 70)
    print("【测试3】闲鱼爬虫 - 持久化模式")
    print("=" * 70)
    
    fish_spider = None
    try:
        fish_spider = FishSpider(headless=False, use_stealth=True)
        print("⏳ 启动闲鱼爬虫...")
        await fish_spider.init_browser()
        
        print("\n✅ 浏览器启动成功")
        print(f"   - Context类型: {type(fish_spider.context).__name__}")
        print(f"   - Page类型: {type(fish_spider.page).__name__}")
        
        # 检查登录状态
        print("\n⏳ 检查登录状态...")
        is_logged_in = await fish_spider.check_login_status()
        
        if is_logged_in:
            print("✅ 闲鱼已登录！")
        else:
            print("❌ 闲鱼未登录")
            print("💡 请运行: python login_helper.py")
        
        # 测试人类行为模拟
        print("\n⏳ 测试人类行为模拟...")
        await fish_spider.human_delay(1.0, 2.0)
        await fish_spider.human_mouse_move(400, 300)
        await fish_spider.human_scroll(200)
        print("✅ 人类行为模拟完成")
        
        # 保持浏览器打开5秒以便观察
        print("\n⏳ 浏览器窗口将保持5秒...")
        await asyncio.sleep(5)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if fish_spider:
            await fish_spider.close()
            print("\n✅ 闲鱼爬虫已关闭")
    
    # 测试4: 验证持久化数据
    print("\n" + "=" * 70)
    print("【测试4】验证持久化数据")
    print("=" * 70)
    
    if os.path.exists(USER_DATA_PATH):
        files = os.listdir(USER_DATA_PATH)
        print(f"✅ 用户数据目录已创建")
        print(f"📁 文件/文件夹数量: {len(files)}")
        
        # 查找关键文件
        key_paths = [
            os.path.join(USER_DATA_PATH, "Default"),
            os.path.join(USER_DATA_PATH, "Default", "Cookies"),
            os.path.join(USER_DATA_PATH, "Default", "Local Storage"),
        ]
        
        for path in key_paths:
            if os.path.exists(path):
                print(f"   ✅ {os.path.basename(path)} - 存在")
            else:
                print(f"   ⚠️  {os.path.basename(path)} - 不存在")
        
        print("\n💡 提示:")
        print("   - 如果看到Cookies和Local Storage，说明持久化成功")
        print("   - 下次启动将自动复用这些登录数据")
    else:
        print("❌ 用户数据目录未创建")
    
    # 总结
    print("\n" + "=" * 70)
    print("🎉 测试完成")
    print("=" * 70)
    print("\n下一步:")
    print("1. 如果提示未登录，运行: python login_helper.py")
    print("2. 登录成功后，再次运行此测试验证自动登录")
    print("3. 运行主程序: python main.py")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_persistent_login())
