"""
🔐 登录辅助脚本（工业级增强版）
用于首次人工登录小红书和闲鱼，保存Session到持久化目录

新特性（2025-12-31）：
- ✅ 修复context.close()破坏持久化问题
- 🩺 集成Session健康监控
- 📊 登录后自动验证和健康检查
- 💾 96.7MB+持久化缓存高效复用

使用方法：
1. 运行：python login_helper.py
2. 选择平台（小红书/闲鱼）
3. 在弹出的浏览器窗口中手动登录（扫码/短信验证）
4. 登录成功后按Enter键，脚本会保存Session
5. 后续爬虫会自动复用登录状态

注意：
- 需要保持浏览器窗口可见（headless=False）
- 登录数据保存在 ./browser_profile 目录（96.7MB+）
- 如需重新登录，删除该目录即可
- 建议每周运行一次维护Session活跃度
"""

import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from config import USER_DATA_PATH, EDGE_PATH
import os

# 导入Session监控
try:
    from scrapers.session_monitor import SessionHealthMonitor
    HAS_MONITOR = True
except:
    HAS_MONITOR = False
    print("⚠️ Session监控模块未找到，将跳过健康检查")


class LoginHelper:
    """登录辅助工具"""
    
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    def _detect_edge_path(self) -> str:
        """智能检测Edge路径（与主爬虫一致：配置 > 注册表 > 环境变量 > 默认路径）。"""
        import subprocess

        if EDGE_PATH and os.path.exists(EDGE_PATH):
            return EDGE_PATH

        reg_keys = [
            r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe',
            r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe',
            r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe',
        ]
        for reg_key in reg_keys:
            try:
                result = subprocess.run(
                    ['reg', 'query', reg_key, '/ve'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode != 0:
                    continue
                for line in result.stdout.split('\n'):
                    if 'REG_SZ' in line:
                        path = line.split('REG_SZ')[-1].strip().strip('"')
                        if os.path.exists(path):
                            return path
            except Exception:
                continue

        search_paths = [
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
        program_files = os.environ.get('PROGRAMFILES', '')
        program_files_x86 = os.environ.get('PROGRAMFILES(X86)', '')
        if program_files:
            search_paths.insert(0, os.path.join(program_files, r"Microsoft\Edge\Application\msedge.exe"))
        if program_files_x86:
            search_paths.insert(0, os.path.join(program_files_x86, r"Microsoft\Edge\Application\msedge.exe"))

        for path in search_paths:
            if os.path.exists(path):
                return path

        raise RuntimeError(
            "❌ Microsoft Edge浏览器未找到！\n"
            "请安装Microsoft Edge或在config.py中配置EDGE_PATH。"
        )
    
    async def init_browser(self):
        """初始化浏览器（可见模式）"""
        print("\n⏳ 正在启动浏览器（可见模式，Edge）...")
        
        self.playwright = await async_playwright().start()
        
        edge_path = self._detect_edge_path()
        
        print(f"📱 使用浏览器：🌐 Microsoft Edge")
        print(f"📁 浏览器路径：{edge_path}")
        print(f"💾 用户数据目录：{USER_DATA_PATH}")
        
        # 确保用户数据目录存在
        os.makedirs(USER_DATA_PATH, exist_ok=True)
        
        # 启动持久化上下文（与爬虫使用相同配置）
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_PATH,
            executable_path=edge_path,  # 使用Edge
            headless=False,  # 必须可见才能手动登录
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ],
            viewport={'width': 1280, 'height': 800},
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
        )
        
        # 应用Stealth反检测（修复版）
        try:
            stealth_patcher = Stealth()
            await stealth_patcher.apply_stealth_async(self.context)
            print("✅ Stealth反检测已应用")
        except Exception as e:
            print(f"⚠️ Stealth应用失败: {e}")
        
        # 获取第一个页面
        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
        
        print("✅ 浏览器启动成功\n")
    
    async def login_xiaohongshu(self):
        """登录小红书"""
        print("=" * 60)
        print("🔴 小红书登录")
        print("=" * 60)
        
        # 访问小红书
        print("\n⏳ 正在打开小红书...")
        await self.page.goto("https://www.xiaohongshu.com/", wait_until='domcontentloaded')
        await asyncio.sleep(3)
        
        print("\n" + "=" * 60)
        print("📱 请在浏览器窗口中完成以下操作：")
        print("=" * 60)
        print("1. 点击右上角「登录」按钮")
        print("2. 选择登录方式（扫码/短信验证码）")
        print("3. 完成验证并登录成功")
        print("4. 确认看到您的头像和用户名")
        print("=" * 60)
        
        input("\n✅ 登录完成后，按 Enter 键继续...")
        
        # 验证登录状态
        await asyncio.sleep(2)
        is_logged_in = await self._check_xiaohongshu_login()
        
        if is_logged_in:
            print("\n✅ 小红书登录成功！Session已保存到本地。")
            
            # 执行健康检查
            if HAS_MONITOR:
                await self._perform_health_check("xiaohongshu")
            print(f"💾 数据位置：{USER_DATA_PATH}")
            print("🎉 后续运行爬虫时会自动复用登录状态！")
        else:
            print("\n⚠️ 未检测到登录状态，请确认是否登录成功。")
    
    async def login_xianyu(self):
        """登录闲鱼"""
        print("=" * 60)
        print("🐟 闲鱼登录")
        print("=" * 60)
        
        # 访问闲鱼
        print("\n⏳ 正在打开闲鱼...")
        await self.page.goto("https://www.goofish.com/", wait_until='domcontentloaded')
        await asyncio.sleep(3)
        
        print("\n" + "=" * 60)
        print("📱 请在浏览器窗口中完成以下操作：")
        print("=" * 60)
        print("1. 点击右上角「登录」按钮")
        print("2. 使用淘宝账号登录（扫码/密码）")
        print("3. 完成安全验证")
        print("4. 确认登录成功")
        print("=" * 60)
        
        input("\n✅ 登录完成后，按 Enter 键继续...")
        
        # 验证登录状态
        await asyncio.sleep(2)
        is_logged_in = await self._check_xianyu_login()

        if is_logged_in:
            print("\n✅ 闲鱼登录成功！Session已保存到本地。")

            # 执行健康检查
            if HAS_MONITOR:
                await self._perform_health_check("xianyu")
            print(f"💾 数据位置：{USER_DATA_PATH}")
            print("🎉 后续运行爬虫时会自动复用登录状态！")
        else:
            print("\n⚠️ 未检测到登录状态，请确认是否登录成功。")
    
    async def _perform_health_check(self, platform: str):
        """执行Session健康检查"""
        try:
            print("\n🩺 正在进行Session健康检查...")
            monitor = SessionHealthMonitor(self.context, platform)
            report = await monitor.check_session_health()
            
            print(monitor.get_health_summary())
            
            # 保存报告
            import json
            report_file = f"session_health_{platform}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n📄 详细报告已保存到: {report_file}")
        
        except Exception as e:
            print(f"⚠️ 健康检查失败: {e}")
    
    async def _check_xiaohongshu_login(self) -> bool:
        """检查小红书登录状态"""
        try:
            # 刷新页面验证
            await self.page.goto("https://www.xiaohongshu.com/", wait_until='domcontentloaded')
            await asyncio.sleep(2)
            
            # 查找登录特征
            selectors = [
                'div.avatar',
                'div.user-avatar',
                'img.avatar-img',
                'div.user-info',
            ]
            
            for selector in selectors:
                try:
                    is_visible = await self.page.locator(selector).is_visible(timeout=2000)
                    if is_visible:
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    async def _check_xianyu_login(self) -> bool:
        """检查闲鱼登录状态"""
        try:
            # 刷新页面验证
            await self.page.goto("https://www.goofish.com/", wait_until='domcontentloaded')
            await asyncio.sleep(2)
            
            # 查找登录特征
            selectors = [
                'div.user-avatar',
                'div.user-info',
                'img.avatar',
                'span.user-nick',
            ]
            
            for selector in selectors:
                try:
                    is_visible = await self.page.locator(selector).is_visible(timeout=2000)
                    if is_visible:
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    async def close(self):
        """关闭浏览器（持久化上下文）
        
        ⚠️ 重要：使用 launch_persistent_context 时，不能调用 context.close()
        否则会破坏登录状态！应该只停止 Playwright 实例。
        """
        try:
            # ❌ 不能关闭 context，否则登录状态会丢失
            # if self.context:
            #     await self.context.close()
            
            # ✅ 只停止 Playwright 实例
            if self.playwright:
                try:
                    await self.playwright.stop()
                except:
                    pass
        except:
            pass
        print("🔌 浏览器已关闭（登录状态已安全保存）")


async def main():
    """主函数"""
    helper = LoginHelper()
    
    try:
        await helper.init_browser()
        
        print("\n" + "=" * 60)
        print("🔐 登录辅助脚本")
        print("=" * 60)
        print("请选择要登录的平台：")
        print("1. 小红书")
        print("2. 闲鱼")
        print("3. 两个都登录")
        print("=" * 60)
        
        choice = input("\n请输入选项 (1/2/3): ").strip()
        
        if choice == "1":
            await helper.login_xiaohongshu()
        elif choice == "2":
            await helper.login_xianyu()
        elif choice == "3":
            await helper.login_xiaohongshu()
            print("\n" + "="*60 + "\n")
            await helper.login_xianyu()
        else:
            print("❌ 无效选项")
        
        print("\n" + "=" * 60)
        print("🎉 登录流程完成！")
        print("=" * 60)
        print("💡 提示：")
        print("   - Session已保存，后续运行爬虫会自动使用")
        print("   - 如需重新登录，删除 ./browser_profile 目录")
        print("   - 建议定期维护登录状态（每周运行一次此脚本）")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
    finally:
        print("\n⏳ 5秒后自动关闭浏览器...")
        await asyncio.sleep(5)
        await helper.close()
        print("✅ 浏览器已关闭")


if __name__ == "__main__":
    asyncio.run(main())
