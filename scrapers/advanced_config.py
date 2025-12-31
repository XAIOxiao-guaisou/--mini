"""
🔥 高级爬虫配置和工具库
包含反爬虫对抗、智能重试、代理管理等机制
"""

import random
import time
from typing import List, Dict, Optional

# 📱 高级 User-Agent 池（真实2025年客户端特征）
PREMIUM_USER_AGENTS = [
    # iPhone 用户
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    
    # Android 用户
    "Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6168.240 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6168.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; POCO X7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    
    # Windows 桌面版
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    
    # macOS 用户
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

# 🌐 免费代理池（可选，需要更新）
FREE_PROXIES = [
    # 注：实际使用时需要更新为有效的代理
    # "http://proxy1:8080",
    # "http://proxy2:8080",
]

# 📏 高级 Viewport 配置
PREMIUM_VIEWPORTS = [
    {"width": 390, "height": 844},    # iPhone 14/15
    {"width": 430, "height": 932},    # iPhone 15 Plus
    {"width": 393, "height": 873},    # Pixel 9
    {"width": 412, "height": 915},    # Android 通用
    {"width": 1920, "height": 1080},  # 桌面 FHD
    {"width": 2560, "height": 1440},  # 桌面 QHD
]

# ⏱️ 智能延迟配置
class DelayManager:
    """智能延迟管理器"""
    
    def __init__(self, min_delay: float = 1.0, max_delay: float = 5.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.base_delay = (min_delay + max_delay) / 2
        self.retry_count = 0
    
    def get_delay(self, retry_count: int = 0) -> float:
        """获取动态延迟时间（指数退避）"""
        if retry_count == 0:
            # 正常延迟：加入随机因子
            return random.uniform(self.min_delay, self.max_delay)
        else:
            # 重试延迟：指数退避
            backoff = 2 ** min(retry_count, 5)  # 最多 2^5 = 32x
            return min(self.base_delay * backoff, 60)  # 最多 60 秒
    
    def sleep(self, retry_count: int = 0):
        """执行延迟"""
        delay = self.get_delay(retry_count)
        time.sleep(delay)
        return delay


# 🎯 请求头构造器
class HeaderBuilder:
    """构造真实的请求头"""
    
    @staticmethod
    def get_headers(user_agent: Optional[str] = None) -> Dict[str, str]:
        """生成伪装的请求头"""
        if not user_agent:
            user_agent = random.choice(PREMIUM_USER_AGENTS)
        
        return {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Sec-Ch-Ua": '"Not_A Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
        }
    
    @staticmethod
    def get_mobile_headers(user_agent: Optional[str] = None) -> Dict[str, str]:
        """移动端请求头"""
        headers = HeaderBuilder.get_headers(user_agent)
        headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.xiaohongshu.com/",
            "Origin": "https://www.xiaohongshu.com",
        })
        return headers


# 🔄 重试管理器
class RetryManager:
    """智能重试管理器"""
    
    def __init__(self, max_retries: int = 5, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """执行函数，自动重试"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    wait_time = (self.backoff_factor ** attempt) * (1 + random.random())
                    print(f"⚠️ 第 {attempt + 1} 次重试失败，{wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ 重试 {self.max_retries} 次后仍失败")
        
        raise last_exception


# 🎨 响应验证器
class ResponseValidator:
    """验证爬虫响应的有效性"""
    
    @staticmethod
    def is_blocked(page_content: str) -> bool:
        """检测是否被反爬虫拦截"""
        blocked_keywords = [
            "请稍后再试",
            "访问受限",
            "被系统拦截",
            "验证请求",
            "人机验证",
            "异常登录",
            "请勿频繁操作",
        ]
        return any(keyword in page_content for keyword in blocked_keywords)
    
    @staticmethod
    def has_content(page_content: str) -> bool:
        """检查页面是否有有效内容"""
        return len(page_content.strip()) > 100
    
    @staticmethod
    def validate_json(data: dict, required_fields: List[str]) -> bool:
        """验证 JSON 数据"""
        return all(field in data for field in required_fields)


# 🔐 IP 轮换管理
class IPRotationManager:
    """IP 轮换管理器"""
    
    def __init__(self, proxies: Optional[List[str]] = None):
        self.proxies = proxies or FREE_PROXIES
        self.current_proxy_idx = 0
    
    def get_next_proxy(self) -> Optional[str]:
        """获取下一个代理"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_proxy_idx]
        self.current_proxy_idx = (self.current_proxy_idx + 1) % len(self.proxies)
        return proxy
    
    def reset(self):
        """重置代理索引"""
        self.current_proxy_idx = 0


# 📊 请求统计
class RequestStats:
    """请求统计"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.blocked_requests = 0
        self.retry_count = 0
    
    def record_success(self):
        self.total_requests += 1
        self.successful_requests += 1
    
    def record_failure(self):
        self.total_requests += 1
        self.failed_requests += 1
    
    def record_blocked(self):
        self.blocked_requests += 1
    
    def record_retry(self):
        self.retry_count += 1
    
    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests * 100
    
    def __str__(self):
        return f"""
📊 请求统计:
  • 总请求数: {self.total_requests}
  • 成功: {self.successful_requests}
  • 失败: {self.failed_requests}
  • 被拦截: {self.blocked_requests}
  • 重试次数: {self.retry_count}
  • 成功率: {self.get_success_rate():.1f}%
"""


# 🌟 浏览器配置优化
BROWSER_LAUNCH_ARGS = [
    # 性能优化
    '--disable-dev-shm-usage',           # 禁用共享内存（Windows 友好）
    '--no-sandbox',                      # 禁用沙箱（加速启动）
    '--disable-gpu',                     # 禁用 GPU（减少内存）
    
    # 反检测
    '--disable-blink-features=AutomationControlled',
    '--hide-scrollbars',                 # 隐藏滚动条
    '--disable-sync',                    # 禁用同步
    '--disable-extensions',              # 禁用扩展
    
    # 内容加载优化
    '--disable-images',                  # 禁用图片（加速）
    '--disable-plugins',                 # 禁用插件
    '--disable-java',                    # 禁用 Java
    '--disable-default-apps',
    
    # 网络优化
    '--dns-prefetch-disable',
    '--disable-preconnect',
    
    # 其他
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-prompt-on-repost',
]

# 仅禁用图片的轻量级配置
LIGHTWEIGHT_BROWSER_ARGS = [
    '--disable-images',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-gpu',
    '--no-first-run',
]


if __name__ == '__main__':
    print("🔥 高级爬虫工具库已加载")
    print(f"✅ User-Agent 池: {len(PREMIUM_USER_AGENTS)} 个")
    print(f"✅ Viewport 池: {len(PREMIUM_VIEWPORTS)} 个")
    print(f"✅ 代理池: {len(FREE_PROXIES)} 个")
