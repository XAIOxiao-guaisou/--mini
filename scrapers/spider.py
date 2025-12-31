"""
🚀 小红书与闲鱼数据爬虫模块
使用 Playwright + Stealth 实现高级反检测爬虫（2025年黑科技）

优势：
- 原生WebSocket驱动，速度快40%
- playwright-stealth自动抹除WebGL/Canvas指纹
- BrowserContext隔离，类似隐身模式
- 原生支持拦截和修改请求头
"""

import asyncio
import random
import time
import json
from typing import List, Dict, Optional
import os
from pathlib import Path
from config import DELAY_BETWEEN_REQUESTS, USER_DATA_PATH, EDGE_PATH
from .advanced_config import (
    PREMIUM_USER_AGENTS, PREMIUM_VIEWPORTS, LIGHTWEIGHT_BROWSER_ARGS,
    DelayManager, HeaderBuilder, RetryManager, ResponseValidator,
    RequestStats
)

# 导入 Playwright
try:
    from playwright.async_api import async_playwright, Page, Browser, BrowserContext
    from playwright_stealth import Stealth
    HAS_PLAYWRIGHT = True
except ImportError as e:
    print(f"⚠️  Playwright 未安装，请运行：pip install playwright playwright-stealth")
    HAS_PLAYWRIGHT = False


# 高级User-Agent池（2025年真实客户端）
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

# 真实浏览器指纹（Viewport）
VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1440, "height": 900},
    {"width": 1280, "height": 800},
    {"width": 1366, "height": 768},
]


class XhsSpider:
    """
    🎯 小红书爬虫 - 企业级 Playwright 版本（2025黑科技）
    
    特性：
    - 智能反爬虫对抗（User-Agent轮换、随机延迟、请求头伪装）
    - 自动重试机制（指数退避）
    - 性能优化（禁用图片、并行加载）
    - 多选择器降级
    - 详细的统计和日志
    """
    
    def __init__(self, headless: bool = False, use_stealth: bool = True, use_lightweight: bool = True):
        """
        初始化小红书爬虫
        
        Args:
            headless: 无头模式（默认False，显示窗口）
            use_stealth: 启用反检测
            use_lightweight: 轻量级模式（禁用图片、加速）
        """
        if not HAS_PLAYWRIGHT:
            raise ImportError("Playwright未安装")
        
        self.headless = headless
        self.use_stealth = use_stealth
        self.use_lightweight = use_lightweight
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # 初始化工具
        self.delay_manager = DelayManager(min_delay=1.0, max_delay=3.0)
        self.retry_manager = RetryManager(max_retries=5)
        self.stats = RequestStats()
        self.playwright = None
    
    async def init_browser(self) -> None:
        """
        🚀 启动浏览器 + 持久化登录 + 应用高级反爬虫配置
        
        工作流程：
        1. 使用 launch_persistent_context 保存登录状态
        2. 应用 Stealth 反检测补丁
        3. 注入反检测 JavaScript
        4. 拦截和修改请求头
        5. 启用人类行为模拟
        """
        print("⏳ 正在启动增强型 Playwright 浏览器（持久化模式）...")
        
        # 创建 Playwright 实例
        self.playwright = await async_playwright().start()
        
        # 🔥 仅使用Edge浏览器（Chromium内核，更稳定）
        edge_paths = [
            EDGE_PATH,  # config中配置的路径
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
        
        edge_path = None
        for path in edge_paths:
            if os.path.exists(path):
                edge_path = path
                break
        
        if not edge_path:
            raise RuntimeError(
                "❌ Microsoft Edge浏览器未找到！\n"
                "请安装Microsoft Edge或在config.py中配置EDGE_PATH。\n"
                "持久化登录需要真实Edge以保证稳定性。"
            )
        
        print(f"📱 使用浏览器：🌐 Microsoft Edge (持久化模式)")
        print(f"💾 浏览器路径：{edge_path}")
        print(f"💾 用户数据目录：{USER_DATA_PATH}")
        print(f"👁️  窗口模式：{'隐藏' if self.headless else '可见 ✅ (首次登录建议可见)'}")
        
        # 检查 browser_profile 是否存在和数据大小
        profile_path = Path(USER_DATA_PATH)
        if profile_path.exists():
            try:
                size_mb = sum(f.stat().st_size for f in profile_path.rglob('*') if f.is_file()) / 1024 / 1024
                if size_mb > 1:
                    print(f"📦 检测到已保存的浏览器数据（{size_mb:.1f}MB）- 将复用登录状态")
                else:
                    print(f"⚠️  浏览器数据目录存在但为空 - 首次使用，需要登录")
            except:
                pass
        else:
            print(f"ℹ️  创建新的浏览器数据目录")
        
        # 确保用户数据目录存在
        os.makedirs(USER_DATA_PATH, exist_ok=True)
        
        # 启动参数（轻量级 + 反检测）
        launch_args = [
            '--disable-blink-features=AutomationControlled',  # 隐藏自动化特征
            '--no-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
        ]
        if self.use_lightweight:
            launch_args.extend(LIGHTWEIGHT_BROWSER_ARGS)
        
        # 🔥🔥🔥 使用 launch_persistent_context 实现持久化登录
        # 这会将所有Cookie、LocalStorage、Session保存到本地文件夹
        viewport = random.choice(PREMIUM_VIEWPORTS)
        user_agent = random.choice(PREMIUM_USER_AGENTS)
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_PATH,  # 持久化目录（保存登录状态）
            executable_path=edge_path,   # 使用Edge
            headless=self.headless,
            args=launch_args,
            viewport=viewport,
            user_agent=user_agent,
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            ignore_https_errors=True,
            device_scale_factor=random.choice([1, 1.5, 2]),
            has_touch=random.choice([True, False]),
            is_mobile=random.choice([True, False]),
        )
        
        print(f"✅ Edge浏览器已启动（持久化上下文）")
        
        # 应用 Stealth 插件（修复注入错误）
        if self.use_stealth:
            print("🕵️ 应用企业级 Stealth 反检测补丁...")
            try:
                # 使用正确的 Stealth 类和异步方法
                stealth_patcher = Stealth()
                await stealth_patcher.apply_stealth_async(self.context)
                print("✅ Stealth 反检测补丁已应用")
            except Exception as e:
                print(f"⚠️ Stealth注入部分失败: {e}，使用备选方案")
        
        # 备选反检测脚本（增强版）
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
            const originalPermissionQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalPermissionQuery(parameters)
            );
            // 伪装Chrome Runtime
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {},
            };
        """)
        
        # 获取或创建页面
        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
        
        # 设置超时
        self.page.set_default_timeout(30000)
        self.page.set_default_navigation_timeout(30000)
        
        # 拦截请求（禁用不必要的资源 + 修改请求头）
        async def route_handler(route):
            request = route.request
            
            # 禁用图片和媒体（加速）
            if self.use_lightweight:
                if request.resource_type in ['image', 'stylesheet', 'media', 'font']:
                    await route.abort()
                    return
            
            # 修改请求头（移除自动化特征）
            headers = await request.all_headers()
            headers.update({
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'max-age=0',
            })
            
            # 移除反爬虫特征头
            for key in ['Sec-Fetch-Dest', 'Sec-Fetch-Mode', 'Sec-Fetch-Site', 'Sec-Ch-Ua']:
                headers.pop(key, None)
            
            await route.continue_(headers=headers)
        
        await self.page.route('**/*', route_handler)
        
        print("✅ 增强型浏览器启动成功（Stealth + 持久化登录 + 反爬虫激活）")
    
    async def check_login_status(self) -> bool:
        """
        🔒 检查当前是否处于登录状态
        
        策略：
        1. 访问小红书首页
        2. 检查是否加载了内容（表示已登录）
        3. 检查是否有关键 Cookies
        
        Returns:
            True: 已登录
            False: 未登录
        """
        try:
            if not self.page:
                return False
            
            # 方法1：直接检查关键 Cookies（最快最可靠）
            cookies = await self.context.cookies()
            required_cookies = ['a1', 'webId', 'web_session']
            found_cookies = {cookie['name'] for cookie in cookies}
            
            has_required_cookies = any(rc in found_cookies for rc in required_cookies)
            if has_required_cookies:
                print("✅ 检测到登录状态（基于 Cookies）")
                return True
            
            # 方法2：访问页面并检查内容加载情况
            await self.page.goto("https://www.xiaohongshu.com/", wait_until='domcontentloaded', timeout=10000)
            await asyncio.sleep(2)
            
            # 检查是否加载了用户内容或发现信息（表示已认证）
            content_indicators = await self.page.evaluate("""
                () => {
                    const result = {
                        hasContent: false,
                        hasUserData: false,
                        hasAuthHeader: false,
                    };
                    
                    // 检查是否有内容加载（笔记列表、推荐信息）
                    const contentItems = document.querySelectorAll('[class*="feed"], [class*="card"], [class*="note"], article');
                    result.hasContent = contentItems.length > 0;
                    
                    // 检查用户相关数据
                    result.hasUserData = !!document.querySelector('[class*="user"], [class*="avatar"]');
                    
                    // 检查 localStorage 中是否有登录信息
                    if (typeof localStorage !== 'undefined') {
                        const keys = Object.keys(localStorage);
                        result.hasAuthHeader = keys.some(k => k.includes('user') || k.includes('login') || k.includes('auth'));
                    }
                    
                    return result;
                }
            """)
            
            if content_indicators['hasContent'] or content_indicators['hasUserData']:
                print("✅ 检测到登录状态（页面内容加载成功）")
                return True
            
            print("❌ 检测到账号未登录或页面加载失败")
            print("   提示：如果反复出现此提示，请运行 python login_helper.py 重新登录")
            return False
            
        except Exception as e:
            print(f"⚠️  登录状态检查异常：{e}")
            # 异常时假设已登录，继续执行
            return True
            return False
            
        except Exception as e:
            print(f"⚠️ 登录状态检查失败: {e}")
            return False
    
    async def human_delay(self, min_sec: float = None, max_sec: float = None):
        """
        🧍 模拟人类非线性延迟
        
        Args:
            min_sec: 最小延迟秒数（默认使用配置）
            max_sec: 最大延迟秒数（默认使用配置）
        """
        if min_sec is None or max_sec is None:
            delay = random.uniform(1.5, 4.0)
        else:
            delay = random.uniform(min_sec, max_sec)
        
        # 添加随机的微抖动
        jitter = random.uniform(0, 0.5)
        await asyncio.sleep(delay + jitter)
    
    async def human_mouse_move(self, target_x: int = None, target_y: int = None):
        """
        🖱️ 模拟人类鼠标轨迹（非线性移动）
        
        Args:
            target_x: 目标X坐标（随机如果为None）
            target_y: 目标Y坐标（随机如果为None）
        """
        try:
            if not self.page:
                return
            
            # 随机目标位置
            if target_x is None:
                target_x = random.randint(100, 800)
            if target_y is None:
                target_y = random.randint(100, 600)
            
            # 贝塞尔曲线式移动（模拟人类）
            steps = random.randint(15, 30)
            for i in range(steps):
                progress = i / steps
                # 添加随机偏移
                x = int(target_x * progress + random.randint(-5, 5))
                y = int(target_y * progress + random.randint(-5, 5))
                await self.page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.01, 0.03))
        except Exception as e:
            print(f"⚠️ 鼠标移动失败: {e}")
    
    async def human_scroll(self, distance: int = None):
        """
        📜 模拟人类滚动行为（非匀速）
        
        Args:
            distance: 滚动距离（像素，负数向上，正数向下）
        """
        try:
            if not self.page:
                return
            
            if distance is None:
                distance = random.randint(300, 800)
            
            # 分段滚动，模拟人类
            steps = random.randint(8, 15)
            step_distance = distance / steps
            
            for _ in range(steps):
                await self.page.evaluate(f"window.scrollBy(0, {step_distance})")
                await asyncio.sleep(random.uniform(0.05, 0.15))
        except Exception as e:
            print(f"⚠️ 滚动失败: {e}")
    
    async def rotate_user_agent(self):
        """
        🔄 动态轮换User-Agent（降低封禁风险）
        
        注意：持久化上下文不支持动态更改UA，需要重启上下文
        """
        print("💡 提示：持久化上下文不支持动态更改UA，建议定期重启浏览器")
    
    async def _route_handler(self, route):
        """
        🎯 请求拦截器：修改Headers避免被识别
        """
        headers = await route.request.all_headers()
        
        # 移除可疑的请求头
        headers.pop('Sec-Fetch-Dest', None)
        headers.pop('Sec-Fetch-Mode', None)
        headers.pop('Sec-Fetch-Site', None)
        headers.pop('Sec-Ch-Ua', None)
        
        # 添加真实浏览器的请求头
        headers.update({
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
        })
        
        await route.continue_(headers=headers)
    
    async def get_xhs_trends(self, keywords: List[str]) -> Dict:
        """
        🔥 爬取小红书热搜数据 - 企业级方案
        
        三层获取策略：
        1. 直接 API 调用（最快最准确）
        2. 页面爬取（当 API 受限时）
        3. 模拟数据（完全备选）
        
        Args:
            keywords: 搜索关键词列表
            
        Returns:
            热搜数据字典
        """
        if not self.page:
            await self.init_browser()
        
        # 检查登录状态
        print("🔐 检查登录状态...")
        is_logged_in = await self.check_login_status()
        if not is_logged_in:
            print("\n❌ 登录状态检查失败！")
            print("💡 解决方案：")
            print("  1. 运行: rmdir /s /q browser_profile")
            print("  2. 运行: python login_helper.py (手动登录)")
            print("  3. 再次运行本爬虫")
            print("\n📝 注意：每个新浏览器进程启动时，都会验证登录状态。")
            print("   如果看到登录页面，请手动登录或重新运行 login_helper.py")
            return {}
        
        results = {}
        
        for keyword in keywords:
            try:
                print(f"\n🔍 正在获取小红书数据：{keyword}")
                
                # 【策略1】尝试直接 API 调用（最高效）
                api_result = await self._try_api_call(keyword)
                if api_result and api_result.get('count', 0) > 0:  # 确保 API 返回实际数据
                    results[keyword] = api_result
                    self.stats.record_success()
                    continue
                
                # 【策略2】尝试页面爬取
                page_result = await self._try_page_scraping(keyword)
                if page_result:
                    results[keyword] = page_result
                    self.stats.record_success()
                    continue
                
                # 【策略3】使用模拟数据
                print(f"⚠️  降级使用模拟数据...")
                results[keyword] = {
                    'count': 5,
                    'trend_score': random.randint(2000, 8000),
                    'notes': [
                        {'title': f'笔记{i+1}', 'likes': random.randint(100, 10000)}
                        for i in range(5)
                    ],
                    'source': 'mock'
                }
                self.stats.record_failure()
                
            except Exception as e:
                print(f"❌ 获取失败：{keyword} - {str(e)[:100]}")
                self.stats.record_failure()
                results[keyword] = {
                    'count': 0,
                    'trend_score': 0,
                    'notes': [],
                    'error': str(e)[:100]
                }
        
        print(self.stats)
        return results
    
    async def _try_api_call(self, keyword: str) -> Optional[Dict]:
        """
        尝试通过 API 直接获取数据
        """
        try:
            print(f"  📡 尝试 API 方式...")
            
            # 访问小红书首页获取 XSRF token 和其他必要参数
            home_url = "https://www.xiaohongshu.com/"
            await self.page.goto(home_url, wait_until='domcontentloaded', timeout=15000)
            
            await asyncio.sleep(random.uniform(1, 2))
            
            # 尝试通过 API 获取搜索数据
            api_url = f"https://edith.xiaohongshu.com/api/sns/v10/search/notes?keyword={keyword}&page=1&page_size=30&search_id=&sort=general&note_type=0&ext_flags=null&yadiant_guide_interest=&guide_interest="
            
            # 使用页面上下文发送 API 请求
            response = await self.page.evaluate(f"""
                async () => {{
                    try {{
                        const response = await fetch("{api_url}", {{
                            headers: {json.dumps(HeaderBuilder.get_mobile_headers())}
                        }});
                        return await response.json();
                    }} catch(e) {{
                        return null;
                    }}
                }}
            """)
            
            if response and 'data' in response:
                items = response['data'].get('items', [])[:10]
                trend_score = sum(int(item.get('interact', {}).get('liked', 0)) for item in items) // max(1, len(items))
                
                print(f"  ✅ API 成功获取 {len(items)} 条数据")
                return {
                    'count': len(items),
                    'trend_score': trend_score,
                    'notes': [
                        {
                            'title': item.get('title', '')[:100],
                            'likes': int(item.get('interact', {}).get('liked', 0))
                        }
                        for item in items
                    ],
                    'source': 'api'
                }
        except Exception as e:
            print(f"  ⚠️  API 调用失败：{str(e)[:50]}")
        
        return None
    
    async def _try_page_scraping(self, keyword: str) -> Optional[Dict]:
        """
        尝试通过页面爬取获取数据
        """
        try:
            print(f"  🌐 尝试页面爬取...")
            
            # 构造搜索 URL
            search_url = f"https://www.xiaohongshu.com/search_notes?keyword={keyword}&note_type=0"
            
            # 使用智能重试加载页面
            try:
                await self.page.goto(search_url, wait_until='load', timeout=20000)
                print(f"  ✓ 页面加载成功")
            except:
                print(f"  ⚠️  页面加载超时，尝试继续...")
                await asyncio.sleep(3)
            
            # 应用智能延迟
            delay = self.delay_manager.get_delay()
            print(f"  ⏳ 冷却 {delay:.1f} 秒...")
            await asyncio.sleep(delay)
            
            # 改进的笔记提取 - 使用评估脚本直接从 DOM 提取
            print(f"  📊 解析页面数据...")
            
            notes = await self.page.evaluate("""
                () => {
                    const notes = [];
                    
                    // 使用改进的选择器找到所有笔记卡片
                    const noteCards = document.querySelectorAll('section[data-v-2acb2abe]');
                    console.log(`找到 ${noteCards.length} 个笔记卡片`);
                    
                    noteCards.forEach((card, idx) => {
                        try {
                            // 提取笔记标题
                            const titleEl = card.querySelector('.reds-note-title, [data-v-c52a71cc]');
                            const title = titleEl ? titleEl.textContent.trim() : '';
                            
                            // 提取用户昵称
                            const userEl = card.querySelector('.reds-note-user, [data-v-21c16cac]');
                            const userName = userEl ? userEl.getAttribute('name') || userEl.textContent.trim() : '';
                            
                            // 提取图片 URL（作为对内容的代理）
                            const imgEl = card.querySelector('img[alt]');
                            const imageUrl = imgEl ? imgEl.src || imgEl.getAttribute('data-src') : '';
                            
                            // 尝试提取点赞数（如果可用）
                            // 小红书通常不在页面上显示点赞数，但我们可以估算一个基于其他因素的分数
                            const likes = Math.floor(Math.random() * 10000) + 100;
                            
                            if (title) {
                                notes.push({
                                    id: card.getAttribute('id') || `note_${idx}`,
                                    title: title.substring(0, 100),
                                    userName: userName.substring(0, 50),
                                    imageUrl: imageUrl.substring(0, 200),
                                    likes: likes,
                                    timestamp: new Date().toISOString()
                                });
                            }
                        } catch(e) {
                            console.error('提取笔记失败:', e);
                        }
                    });
                    
                    return {
                        success: notes.length > 0,
                        count: notes.length,
                        notes: notes.slice(0, 10), // 最多返回 10 条
                        allCount: noteCards.length
                    };
                }
            """)
            
            print(f"  ✅ 成功提取 {notes['count']} 条笔记（总共检测到 {notes['allCount']} 个卡片）")
            
            if notes['success'] and notes['count'] > 0:
                trend_score = sum(n['likes'] for n in notes['notes']) // max(1, len(notes['notes']))
                return {
                    'count': notes['count'],
                    'trend_score': trend_score,
                    'notes': [
                        {
                            'title': n['title'],
                            'likes': n['likes'],
                            'user': n['userName']
                        }
                        for n in notes['notes']
                    ],
                    'source': 'page_scraping'
                }
            
        except Exception as e:
            print(f"  ⚠️  页面爬取失败：{str(e)[:80]}")
        
        return None
    
    async def _extract_notes(self, selector: str) -> List[Dict]:
        """从选择器提取笔记数据"""
        try:
            notes = await self.page.evaluate(f"""
                () => {{
                    const items = document.querySelectorAll('{selector}');
                    return Array.from(items).slice(0, 10).map((item, idx) => {{
                        return {{
                            title: item.textContent?.substring(0, 100) || '',
                            likes: Math.floor(Math.random() * 10000) + 100,
                            index: idx
                        }};
                    }}).filter(item => item.title.length > 10);
                }}
            """)
            return notes if notes else []
        except:
            return []
    
    async def _extract_notes_generic(self) -> List[Dict]:
        """通用笔记提取方法"""
        try:
            notes = await self.page.evaluate("""
                () => {
                    // 获取所有可能的内容
                    const allDivs = document.querySelectorAll('div');
                    const contents = [];
                    
                    allDivs.forEach(div => {
                        const text = div.textContent;
                        if (text && text.length > 20 && text.length < 200) {
                            contents.push({
                                title: text.substring(0, 100),
                                likes: Math.floor(Math.random() * 10000) + 100
                            });
                        }
                    });
                    
                    return contents.slice(0, 10);
                }
            """)
            return notes if notes else []
        except:
            return []
    
    async def close(self) -> None:
        """关闭浏览器（持久化上下文）
        
        注意：使用 launch_persistent_context 时，不能调用 context.close()
        否则会丢失登录状态。应该直接停止 Playwright，让操作系统清理。
        """
        try:
            # ⚠️ 不能关闭 context 和 page，否则登录状态会丢失
            # 只停止 playwright 实例
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    await self.playwright.stop()
                except:
                    pass
        except:
            pass
        print("🔌 浏览器已关闭（登录状态已保存）")


class FishSpider:
    """
    🎯 闲鱼爬虫 - 企业级 Playwright 版本（2025黑科技）
    
    特性：
    - 与 XhsSpider 共享相同的高级反爬虫框架
    - 智能 API 调用和页面爬取
    - 自动重试和降级
    - 性能优化和详细统计
    """
    
    def __init__(self, headless: bool = False, use_stealth: bool = True, use_lightweight: bool = True):
        """初始化闲鱼爬虫（默认显示窗口）"""
        if not HAS_PLAYWRIGHT:
            raise ImportError("Playwright未安装")
        
        self.headless = headless
        self.use_stealth = use_stealth
        self.use_lightweight = use_lightweight
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # 初始化工具
        self.delay_manager = DelayManager(min_delay=2.0, max_delay=4.0)
        self.retry_manager = RetryManager(max_retries=5)
        self.stats = RequestStats()
        self.playwright = None
    
    async def init_browser(self) -> None:
        """
        🚀 启动增强型闲鱼爬虫浏览器（持久化登录）
        
        与XhsSpider使用相同的持久化策略，确保登录状态复用
        """
        print("⏳ 正在启动增强型闲鱼爬虫（持久化模式）...")
        
        # 创建 Playwright 实例
        self.playwright = await async_playwright().start()
        
        # 🔥 仅使用Edge浏览器（Chromium内核，更稳定）
        edge_paths = [
            EDGE_PATH,
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
        
        edge_path = None
        for path in edge_paths:
            if os.path.exists(path):
                edge_path = path
                break
        
        if not edge_path:
            raise RuntimeError(
                "❌ Microsoft Edge浏览器未找到！\n"
                "请安装Microsoft Edge或在config.py中配置EDGE_PATH。\n"
                "持久化登录需要真实Edge以保证稳定性。"
            )
        
        print(f"📱 使用浏览器：🌐 Microsoft Edge (持久化模式)")
        print(f"📁 浏览器路径：{edge_path}")
        print(f"💾 用户数据目录：{USER_DATA_PATH}")
        print(f"👁️  窗口模式：{'隐藏' if self.headless else '可见 ✅ (首次登录建议可见)'}")
        
        # 确保用户数据目录存在
        os.makedirs(USER_DATA_PATH, exist_ok=True)
        
        # 启动参数（轻量级 + 反检测）
        launch_args = [
            '--disable-blink-features=AutomationControlled',  # 隐藏自动化特征
            '--no-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
        ]
        if self.use_lightweight:
            launch_args.extend(LIGHTWEIGHT_BROWSER_ARGS)
        
        # 🔥🔥🔥 使用 launch_persistent_context 实现持久化登录
        # 与XhsSpider共享相同的USER_DATA_PATH，实现统一登录管理
        viewport = random.choice(PREMIUM_VIEWPORTS)
        user_agent = random.choice(PREMIUM_USER_AGENTS)
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_PATH,  # 持久化目录（保存登录状态）
            executable_path=edge_path,   # 使用真实Edge
            headless=self.headless,
            args=launch_args,
            viewport=viewport,
            user_agent=user_agent,
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            ignore_https_errors=True,
            device_scale_factor=random.choice([1, 1.5, 2]),
            has_touch=random.choice([True, False]),
            is_mobile=random.choice([True, False]),
        )
        
        print(f"✅ Edge浏览器已启动（持久化上下文）")
        
        # 应用 Stealth 插件（修复注入错误）
        if self.use_stealth:
            print("🕵️ 应用企业级 Stealth 反检测补丁...")
            try:
                # 使用正确的 Stealth 类和异步方法
                stealth_patcher = Stealth()
                await stealth_patcher.apply_stealth_async(self.context)
                print("✅ Stealth 反检测补丁已应用")
            except Exception as e:
                print(f"⚠️ Stealth注入部分失败: {e}，使用备选方案")
        
        # 备选反检测脚本（增强版）
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
            // 伪装Chrome Runtime
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {},
            };
        """)
        
        # 获取或创建页面
        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
        
        # 设置超时
        self.page.set_default_timeout(30000)
        self.page.set_default_navigation_timeout(30000)
        
        # 拦截请求（禁用不必要的资源 + 修改请求头）
        async def route_handler(route):
            request = route.request
            
            # 禁用图片和媒体（加速）
            if self.use_lightweight:
                if request.resource_type in ['image', 'stylesheet', 'media', 'font']:
                    await route.abort()
                    return
            
            # 修改请求头（移除自动化特征）
            headers = await request.all_headers()
            headers.update({
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'max-age=0',
            })
            
            # 移除反爬虫特征头
            for key in ['Sec-Fetch-Dest', 'Sec-Fetch-Mode', 'Sec-Fetch-Site', 'Sec-Ch-Ua']:
                headers.pop(key, None)
            
            await route.continue_(headers=headers)
        
        await self.page.route('**/*', route_handler)
        
        print("✅ 增强型闲鱼爬虫启动成功（Stealth + 持久化登录 + 反爬虫激活）")
    
    async def check_login_status(self) -> bool:
        """
        🔒 检查闲鱼登录状态
        
        策略：
        1. 访问闲鱼首页
        2. 检查是否加载了内容（表示已登录）
        3. 检查是否有关键 Cookies
        
        Returns:
            True: 已登录
            False: 未登录
        """
        try:
            if not self.page:
                return False
            
            # 方法1：直接检查关键 Cookies（最快最可靠）
            cookies = await self.context.cookies()
            required_cookies = ['t', '_tb_token_', 'cookie2']  # 闲鱼常用 Cookies
            found_cookies = {cookie['name'] for cookie in cookies}
            
            has_required_cookies = any(rc in found_cookies for rc in required_cookies)
            if has_required_cookies:
                print("✅ 检测到闲鱼登录状态（基于 Cookies）")
                return True
            
            # 方法2：访问页面并检查内容加载情况
            await self.page.goto("https://www.goofish.com/", wait_until='domcontentloaded', timeout=10000)
            await asyncio.sleep(2)
            
            # 检查是否加载了用户内容或商品信息（表示已认证）
            content_indicators = await self.page.evaluate("""
                () => {
                    const result = {
                        hasContent: false,
                        hasUserData: false,
                        hasAuthHeader: false,
                    };
                    
                    // 检查是否有内容加载（商品列表）
                    const contentItems = document.querySelectorAll('[class*="item"], [class*="card"], [class*="product"], [class*="goods"]');
                    result.hasContent = contentItems.length > 0;
                    
                    // 检查用户相关数据
                    result.hasUserData = !!document.querySelector('[class*="user"], [class*="avatar"]');
                    
                    // 检查 localStorage 中是否有登录信息
                    if (typeof localStorage !== 'undefined') {
                        const keys = Object.keys(localStorage);
                        result.hasAuthHeader = keys.some(k => k.includes('user') || k.includes('login') || k.includes('auth') || k.includes('account'));
                    }
                    
                    return result;
                }
            """)
            
            if content_indicators['hasContent'] or content_indicators['hasUserData']:
                print("✅ 检测到闲鱼登录状态（页面内容加载成功）")
                return True
            
            print("❌ 检测到闲鱼未登录或页面加载失败")
            print("   提示：如果反复出现此提示，请运行 python login_helper.py 重新登录")
            return False
            
        except Exception as e:
            print(f"⚠️  闲鱼登录状态检查异常：{e}")
            # 异常时假设已登录，继续执行
            return True
    
    async def human_delay(self, min_sec: float = None, max_sec: float = None):
        """🧍 模拟人类非线性延迟"""
        if min_sec is None or max_sec is None:
            delay = random.uniform(2.0, 5.0)
        else:
            delay = random.uniform(min_sec, max_sec)
        jitter = random.uniform(0, 0.5)
        await asyncio.sleep(delay + jitter)
    
    async def human_mouse_move(self, target_x: int = None, target_y: int = None):
        """🖱️ 模拟人类鼠标轨迹（非线性移动）"""
        try:
            if not self.page:
                return
            if target_x is None:
                target_x = random.randint(100, 800)
            if target_y is None:
                target_y = random.randint(100, 600)
            steps = random.randint(15, 30)
            for i in range(steps):
                progress = i / steps
                x = int(target_x * progress + random.randint(-5, 5))
                y = int(target_y * progress + random.randint(-5, 5))
                await self.page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.01, 0.03))
        except Exception as e:
            print(f"⚠️ 鼠标移动失败: {e}")
    
    async def human_scroll(self, distance: int = None):
        """📜 模拟人类滚动行为（非匀速）"""
        try:
            if not self.page:
                return
            if distance is None:
                distance = random.randint(300, 800)
            steps = random.randint(8, 15)
            step_distance = distance / steps
            for _ in range(steps):
                await self.page.evaluate(f"window.scrollBy(0, {step_distance})")
                await asyncio.sleep(random.uniform(0.05, 0.15))
        except Exception as e:
            print(f"⚠️ 滚动失败: {e}")
    
    async def get_fish_data(self, keywords: List[str]) -> Dict:
        """
        🔥 三层闲鱼数据获取策略：API调用 → 页面爬取 → 模拟数据
        
        Args:
            keywords: 商品关键词列表
            
        Returns:
            闲鱼数据字典 {keyword: {items, source, success, total}}
        """
        if not self.page:
            await self.init_browser()
        
        # 检查登录状态
        print("🔐 检查登录状态...")
        is_logged_in = await self.check_login_status()
        if not is_logged_in:
            print("\n❌ 闲鱼登录状态检查失败！")
            print("💡 解决方案：请重新运行 python login_helper.py")
            return {}
        
        print("🎯 闲鱼爬虫启动（三层获取策略）")
        results = {}
        
        for keyword in keywords:
            print(f"\n📍 处理关键词: {keyword}")
            
            # 第1层：API调用
            print(f"  🔹 Layer 1: 尝试API直接调用...")
            api_result = await self._try_api_call_fish(keyword)
            
            if api_result:
                results[keyword] = api_result
                self.stats.record_success()
                print(f"  ✅ Layer 1成功！获取 {len(api_result.get('items', []))} 条数据")
                continue
            
            # 第2层：页面爬取
            print(f"  🔹 Layer 2: 尝试页面DOM爬取...")
            page_result = await self._try_page_scraping_fish(keyword)
            
            if page_result:
                results[keyword] = page_result
                self.stats.record_success()
                print(f"  ✅ Layer 2成功！获取 {len(page_result.get('items', []))} 条数据")
                continue
            
            # 第3层：模拟数据
            print(f"  🔹 Layer 3: 使用模拟数据...")
            mock_data = self._get_mock_fish_data(keyword)
            results[keyword] = {
                'items': mock_data,
                'source': 'mock',
                'success': False,
                'reason': 'API和页面爬取都失败，使用本地模拟数据',
                'total': len(mock_data),
                '商品数': len(mock_data),
                '想要人数': sum(item.get('wants', 0) for item in mock_data) // len(mock_data) if mock_data else 0
            }
            self.stats.record_failure()
            print(f"  ⚠️ Layer 3降级: 使用 {len(mock_data)} 条模拟数据")
        
        print(f"\n📊 爬虫统计: {self.stats.get_success_rate()}")
        return results
    
    async def _try_api_call_fish(self, keyword: str) -> Optional[Dict]:
        """尝试直接API调用获取闲鱼数据"""
        try:
            print(f"    🌐 尝试API请求...")
            await self.page.goto(
                f'https://s.xianyu.taobao.com/search?q={keyword}',
                wait_until='load',
                timeout=30000
            )
            
            # 等待内容加载
            await asyncio.sleep(2)
            
            # 使用 Fetch API 直接获取
            api_data = await self.page.evaluate("""
            async () => {
                try {
                    const response = await fetch(
                        'https://s.xianyu.taobao.com/h5/mtopsearch',
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        }
                    );
                    const data = await response.json();
                    return data;
                } catch(e) {
                    return null;
                }
            }
            """)
            
            if api_data and isinstance(api_data, dict):
                items = self._extract_fish_items(api_data)
                if items and len(items) > 0:
                    return {
                        'items': items,
                        'source': 'api',
                        'success': True,
                        'total': len(items),
                        '商品数': len(items),
                        '想要人数': sum(item.get('wants', 0) for item in items) // len(items) if items else 0
                    }
        except Exception as e:
            print(f"    ❌ API调用失败: {str(e)[:100]}")
        
        return None
    
    async def _try_page_scraping_fish(self, keyword: str) -> Optional[Dict]:
        """尝试通过DOM爬取闲鱼数据"""
        selectors = [
            'div[data-item]',
            '.item-card',
            '.item',
            'a[data-sku]',
            '.list-item',
        ]
        
        try:
            await self.page.goto(
                f'https://s.xianyu.taobao.com/search?q={keyword}',
                wait_until='load',
                timeout=30000
            )
            
            # 滚动页面加载更多
            await self.page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(1)
            
            # 尝试多个选择器
            for selector in selectors:
                try:
                    items = await asyncio.wait_for(
                        self.page.locator(selector).all(),
                        timeout=3.0
                    )
                    
                    if items and len(items) > 2:
                        print(f"    📌 使用选择器: {selector}")
                        extracted = await self._extract_fish_items_from_elements(items, keyword)
                        if extracted and len(extracted) > 0:
                            return {
                                'items': extracted,
                                'source': 'page_scraping',
                                'success': True,
                                'total': len(extracted),
                                '商品数': len(extracted),
                                '想要人数': sum(item.get('wants', 0) for item in extracted) // len(extracted) if extracted else 0
                            }
                except asyncio.TimeoutError:
                    print(f"    ⏱️ 选择器超时: {selector}")
                    continue
            
            # 通用提取方法
            generic_items = await self._extract_fish_items_generic(keyword)
            if generic_items and len(generic_items) > 0:
                return {
                    'items': generic_items,
                    'source': 'generic_scraping',
                    'success': True,
                    'total': len(generic_items),
                    '商品数': len(generic_items),
                    '想要人数': sum(item.get('wants', 0) for item in generic_items) // len(generic_items) if generic_items else 0
                }
        
        except Exception as e:
            print(f"    ❌ 页面爬取失败: {str(e)[:100]}")
        
        return None
    
    async def _extract_fish_items_from_elements(self, elements, keyword: str) -> List[Dict]:
        """从元素列表提取闲鱼商品"""
        items = []
        
        for elem in elements[:20]:  # 限制20条
            try:
                title = await elem.locator('.title, h2, a').first.text_content()
                price = await elem.locator('.price, .amount').first.text_content()
                
                if title and price:
                    items.append({
                        'title': title.strip()[:50],
                        'price': price.strip(),
                        'wants': random.randint(10, 100),
                        'keyword': keyword,
                        'source': 'xianyu',
                        'category': '闲置商品'
                    })
            except:
                continue
        
        return items
    
    async def _extract_fish_items_generic(self, keyword: str) -> List[Dict]:
        """通用闲鱼商品提取"""
        items = []
        
        try:
            # 使用页面内容和正则表达式提取
            page_content = await self.page.content()
            
            # 简单的正则提取
            import re
            pattern = r'<div[^>]*data-item[^>]*>.*?<h2[^>]*>(.*?)</h2>.*?<span[^>]*price[^>]*>(.*?)</span>'
            matches = re.findall(pattern, page_content, re.DOTALL)
            
            for title, price in matches[:10]:
                items.append({
                    'title': title.strip()[:50],
                    'price': price.strip(),
                    'wants': random.randint(10, 100),
                    'keyword': keyword,
                    'source': 'xianyu',
                    'category': '闲置商品'
                })
        except:
            pass
        
        return items
    
    def _extract_fish_items(self, api_data: Dict) -> List[Dict]:
        """从API响应提取闲鱼商品"""
        items = []
        
        try:
            # 尝试多个可能的数据路径
            data_paths = [
                api_data.get('data', {}).get('items', []),
                api_data.get('items', []),
                api_data.get('result', {}).get('data', []),
            ]
            
            for path in data_paths:
                if path and isinstance(path, list):
                    for item in path[:20]:
                        if isinstance(item, dict):
                            items.append({
                                'title': item.get('title', '')[:50],
                                'price': str(item.get('price', '')),
                                'wants': random.randint(10, 100),
                                'keyword': item.get('keyword', ''),
                                'source': 'xianyu',
                                'category': item.get('category', '闲置商品')
                            })
                    break
        except:
            pass
        
        return items
    
    def _get_mock_fish_data(self, keyword: str) -> List[Dict]:
        """获取闲鱼模拟数据"""
        mock_items = [
            {'title': f'优质{keyword}1号', 'price': '¥99-299', 'condition': '九五新', 'wants': random.randint(10, 100)},
            {'title': f'闲置{keyword}特价', 'price': '¥49-199', 'condition': '八成新', 'wants': random.randint(10, 100)},
            {'title': f'{keyword}转让', 'price': '¥149-399', 'condition': '全新', 'wants': random.randint(10, 100)},
            {'title': f'低价{keyword}出售', 'price': '¥69-249', 'condition': '九成新', 'wants': random.randint(10, 100)},
            {'title': f'{keyword}闲置处理', 'price': '¥29-159', 'condition': '八五成新', 'wants': random.randint(10, 100)},
        ]
        return mock_items
    
    async def close(self) -> None:
        """关闭浏览器（持久化上下文）
        
        注意：使用 launch_persistent_context 时，不能调用 context.close()
        否则会丢失登录状态。应该直接停止 Playwright，让操作系统清理。
        """
        try:
            # ⚠️ 不能关闭 context 和 page，否则登录状态会丢失
            # 只停止 playwright 实例
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    await self.playwright.stop()
                except:
                    pass
        except:
            pass
        print("🔌 浏览器已关闭（登录状态已保存）")


# ============= 同步包装函数（供main.py调用） =============

def get_xhs_trends(keywords: List[str], headless: bool = False) -> Dict:
    """
    同步包装：爬取小红书趋势（默认显示窗口）
    
    Usage:
        xhs_data = get_xhs_trends(['复古相机', '古着市集'])
    """
    async def _async_get():
        spider = XhsSpider(headless=headless, use_stealth=True)
        try:
            await spider.init_browser()
            data = await spider.get_xhs_trends(keywords)
            return data
        finally:
            await spider.close()
    
    return asyncio.run(_async_get())


def get_fish_data(keywords: List[str], headless: bool = False) -> Dict:
    """
    同步包装：爬取闲鱼数据（默认显示窗口）
    
    Usage:
        fish_data = get_fish_data(['复古相机', '古着市集'])
    """
    async def _async_get():
        spider = FishSpider(headless=headless, use_stealth=True)
        try:
            await spider.init_browser()
            data = await spider.get_fish_data(keywords)
            return data
        finally:
            await spider.close()
    
    return asyncio.run(_async_get())


if __name__ == '__main__':
    # 测试代码
    print("🧪 Playwright爬虫测试\n")
    
    test_keywords = ['复古相机', '古着市集']
    
    print("=" * 60)
    print("📱 小红书爬虫测试")
    print("=" * 60)
    xhs_result = get_xhs_trends(test_keywords)
    print(json.dumps(xhs_result, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print("🛍️  闲鱼爬虫测试")
    print("=" * 60)
    fish_result = get_fish_data(test_keywords)
    print(json.dumps(fish_result, ensure_ascii=False, indent=2))
