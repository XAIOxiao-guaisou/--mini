"""
🩺 Session 健康监控系统
实时监控浏览器Session状态，提供自动维护和告警机制

功能：
1. Cookie有效期监控
2. Session活跃度检测
3. 登录状态验证
4. 自动续期建议
5. 健康评分系统

作者：iostoupin Team
日期：2025-12-31
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import BrowserContext, Page


class SessionHealthMonitor:
    """Session健康监控器"""
    
    # 关键Cookie名称（小红书）
    XHS_CRITICAL_COOKIES = ['a1', 'webId', 'web_session', 'xsecappid']
    
    # 关键Cookie名称（闲鱼）
    FISH_CRITICAL_COOKIES = ['_m_h5_tk', '_m_h5_tk_enc', 'cookie2', 'sgcookie']
    
    # 健康阈值
    HEALTH_THRESHOLDS = {
        "excellent": 90,   # 优秀
        "good": 70,        # 良好
        "warning": 50,     # 警告
        "critical": 30,    # 危急
    }
    
    def __init__(self, context: BrowserContext, platform: str = "xiaohongshu"):
        """
        初始化监控器
        
        Args:
            context: Playwright浏览器上下文
            platform: 平台名称 ("xiaohongshu" 或 "xianyu")
        """
        self.context = context
        self.platform = platform
        self.critical_cookies = (
            self.XHS_CRITICAL_COOKIES if platform == "xiaohongshu" 
            else self.FISH_CRITICAL_COOKIES
        )
        self.last_check_time = None
        self.health_history = []
    
    async def check_session_health(self) -> Dict:
        """
        全面检查Session健康状态
        
        Returns:
            健康报告字典
        """
        self.last_check_time = datetime.now()
        
        # 1. 获取所有Cookie
        cookies = await self.context.cookies()
        
        # 2. 分析Cookie健康度
        cookie_health = self._analyze_cookies(cookies)
        
        # 3. 检测关键Cookie
        critical_status = self._check_critical_cookies(cookies)
        
        # 4. 计算过期风险
        expiry_risk = self._calculate_expiry_risk(cookies)
        
        # 5. 检查存储大小
        storage_health = await self._check_storage_size()
        
        # 6. 计算综合健康评分
        health_score = self._calculate_health_score(
            cookie_health, critical_status, expiry_risk, storage_health
        )
        
        # 7. 生成报告
        report = {
            "timestamp": self.last_check_time.isoformat(),
            "platform": self.platform,
            "health_score": health_score,
            "health_level": self._get_health_level(health_score),
            "cookie_count": len(cookies),
            "critical_cookies_present": critical_status["all_present"],
            "missing_cookies": critical_status["missing"],
            "expiring_soon": expiry_risk["expiring_soon"],
            "expired": expiry_risk["expired"],
            "storage_mb": storage_health["size_mb"],
            "recommendations": self._generate_recommendations(
                health_score, critical_status, expiry_risk
            )
        }
        
        # 保存历史
        self.health_history.append(report)
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]
        
        return report
    
    def _analyze_cookies(self, cookies: List[Dict]) -> float:
        """分析Cookie整体健康度（0-100分）"""
        if not cookies:
            return 0.0
        
        # 基础分：有Cookie就给50分
        score = 50.0
        
        # Cookie数量加分（最多20分）
        count_bonus = min(len(cookies) / 20 * 20, 20)
        score += count_bonus
        
        # 有效Cookie比例加分（最多30分）
        valid_count = sum(1 for c in cookies if self._is_cookie_valid(c))
        valid_ratio = valid_count / len(cookies)
        score += valid_ratio * 30
        
        return min(score, 100.0)
    
    def _is_cookie_valid(self, cookie: Dict) -> bool:
        """判断单个Cookie是否有效"""
        # 检查是否有过期时间
        if "expires" in cookie and cookie["expires"] > 0:
            # 检查是否已过期
            expires_timestamp = cookie["expires"]
            if expires_timestamp < time.time():
                return False
        
        # 检查值是否为空
        if not cookie.get("value"):
            return False
        
        return True
    
    def _check_critical_cookies(self, cookies: List[Dict]) -> Dict:
        """检查关键Cookie是否存在"""
        cookie_names = {c["name"] for c in cookies}
        missing = [name for name in self.critical_cookies if name not in cookie_names]
        
        return {
            "all_present": len(missing) == 0,
            "present_count": len(self.critical_cookies) - len(missing),
            "total_count": len(self.critical_cookies),
            "missing": missing
        }
    
    def _calculate_expiry_risk(self, cookies: List[Dict]) -> Dict:
        """计算Cookie过期风险"""
        now = time.time()
        expiring_soon = []  # 7天内过期
        expired = []
        
        for cookie in cookies:
            if "expires" not in cookie or cookie["expires"] <= 0:
                continue  # Session Cookie，不检查过期
            
            expires_timestamp = cookie["expires"]
            time_left = expires_timestamp - now
            
            if time_left < 0:
                expired.append(cookie["name"])
            elif time_left < 7 * 24 * 3600:  # 7天
                days_left = time_left / (24 * 3600)
                expiring_soon.append({
                    "name": cookie["name"],
                    "days_left": round(days_left, 1)
                })
        
        return {
            "expiring_soon": expiring_soon,
            "expired": expired,
            "risk_level": "high" if expired else ("medium" if expiring_soon else "low")
        }
    
    async def _check_storage_size(self) -> Dict:
        """检查浏览器存储大小"""
        try:
            # 获取第一个页面
            pages = self.context.pages
            if not pages:
                page = await self.context.new_page()
                close_after = True
            else:
                page = pages[0]
                close_after = False
            
            # 执行JavaScript获取存储信息
            storage_info = await page.evaluate("""
                () => {
                    let totalSize = 0;
                    
                    // LocalStorage
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        const value = localStorage.getItem(key);
                        totalSize += key.length + (value ? value.length : 0);
                    }
                    
                    // SessionStorage
                    for (let i = 0; i < sessionStorage.length; i++) {
                        const key = sessionStorage.key(i);
                        const value = sessionStorage.getItem(key);
                        totalSize += key.length + (value ? value.length : 0);
                    }
                    
                    return {
                        localStorageItems: localStorage.length,
                        sessionStorageItems: sessionStorage.length,
                        totalSizeBytes: totalSize
                    };
                }
            """)
            
            if close_after:
                await page.close()
            
            size_mb = storage_info["totalSizeBytes"] / (1024 * 1024)
            
            return {
                "size_mb": round(size_mb, 2),
                "local_items": storage_info["localStorageItems"],
                "session_items": storage_info["sessionStorageItems"],
                "health": "good" if size_mb > 0 else "warning"
            }
        
        except Exception as e:
            return {
                "size_mb": 0,
                "local_items": 0,
                "session_items": 0,
                "health": "unknown",
                "error": str(e)
            }
    
    def _calculate_health_score(
        self, 
        cookie_health: float, 
        critical_status: Dict, 
        expiry_risk: Dict, 
        storage_health: Dict
    ) -> float:
        """计算综合健康评分（0-100）"""
        score = 0.0
        
        # Cookie健康度（40%权重）
        score += cookie_health * 0.4
        
        # 关键Cookie存在性（30%权重）
        if critical_status["all_present"]:
            score += 30
        else:
            ratio = critical_status["present_count"] / critical_status["total_count"]
            score += 30 * ratio
        
        # 过期风险（20%权重）
        if expiry_risk["risk_level"] == "low":
            score += 20
        elif expiry_risk["risk_level"] == "medium":
            score += 10
        # high risk不加分
        
        # 存储健康（10%权重）
        if storage_health["health"] == "good":
            score += 10
        elif storage_health["health"] == "warning":
            score += 5
        
        return min(round(score, 1), 100.0)
    
    def _get_health_level(self, score: float) -> str:
        """根据评分获取健康等级"""
        if score >= self.HEALTH_THRESHOLDS["excellent"]:
            return "excellent"
        elif score >= self.HEALTH_THRESHOLDS["good"]:
            return "good"
        elif score >= self.HEALTH_THRESHOLDS["warning"]:
            return "warning"
        else:
            return "critical"
    
    def _generate_recommendations(
        self, 
        health_score: float, 
        critical_status: Dict, 
        expiry_risk: Dict
    ) -> List[str]:
        """生成维护建议"""
        recommendations = []
        
        # 根据健康等级给建议
        if health_score < self.HEALTH_THRESHOLDS["warning"]:
            recommendations.append("⚠️ 健康度较低，建议立即重新登录维护Session")
        
        # 关键Cookie缺失
        if not critical_status["all_present"]:
            missing_str = ", ".join(critical_status["missing"])
            recommendations.append(f"❌ 关键Cookie缺失: {missing_str}，请重新登录")
        
        # 过期风险
        if expiry_risk["expired"]:
            recommendations.append(f"🕐 已过期Cookie: {', '.join(expiry_risk['expired'][:3])}...")
        
        if expiry_risk["expiring_soon"]:
            days = expiry_risk["expiring_soon"][0]["days_left"]
            recommendations.append(f"⏰ 有Cookie将在 {days:.1f} 天后过期，建议刷新Session")
        
        # 常规维护建议
        if health_score >= self.HEALTH_THRESHOLDS["good"]:
            recommendations.append("✅ Session状态良好，建议每周维护一次")
        
        return recommendations
    
    async def verify_login_status(self, url: str) -> Tuple[bool, str]:
        """
        验证登录状态（通过访问页面）
        
        Args:
            url: 验证URL（如小红书首页）
        
        Returns:
            (是否登录, 详细信息)
        """
        try:
            # 获取或创建页面
            pages = self.context.pages
            if not pages:
                page = await self.context.new_page()
                close_after = True
            else:
                page = pages[0]
                close_after = False
            
            # 访问页面
            await page.goto(url, wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(2)
            
            # 检查登录特征
            is_logged_in = await page.evaluate("""
                () => {
                    // 检查是否有用户头像/信息
                    const selectors = [
                        'div.avatar', 'div.user-avatar', 'img.avatar-img',
                        'div.user-info', 'span.user-nick'
                    ];
                    
                    for (const selector of selectors) {
                        const el = document.querySelector(selector);
                        if (el) return true;
                    }
                    
                    // 检查是否有登录按钮（未登录标志）
                    const loginSelectors = ['button.login', 'a.login-btn', 'div.login'];
                    for (const selector of loginSelectors) {
                        const el = document.querySelector(selector);
                        if (el && el.textContent.includes('登录')) return false;
                    }
                    
                    return false;
                }
            """)
            
            if close_after:
                await page.close()
            
            if is_logged_in:
                return True, "✅ 登录状态有效"
            else:
                return False, "❌ 未检测到登录状态"
        
        except Exception as e:
            return False, f"⚠️ 验证失败: {str(e)[:50]}"
    
    def get_health_summary(self) -> str:
        """获取健康状态摘要（彩色文本）"""
        if not self.health_history:
            return "📊 尚未进行健康检查"
        
        latest = self.health_history[-1]
        level = latest["health_level"]
        
        # 选择表情符号
        emoji_map = {
            "excellent": "🟢",
            "good": "🟡",
            "warning": "🟠",
            "critical": "🔴"
        }
        emoji = emoji_map.get(level, "⚪")
        
        summary = f"""
╔════════════════════════════════════════════╗
║  {emoji} Session 健康报告 - {self.platform.upper()}
╠════════════════════════════════════════════╣
║  健康评分: {latest['health_score']}/100 ({level.upper()})
║  Cookie数量: {latest['cookie_count']}
║  关键Cookie: {'✅ 完整' if latest['critical_cookies_present'] else '❌ 缺失'}
║  过期风险: {len(latest['expiring_soon'])} 个即将过期
║  存储大小: {latest['storage_mb']} MB
╠════════════════════════════════════════════╣
║  💡 建议:
"""
        
        for rec in latest["recommendations"]:
            summary += f"║    {rec}\n"
        
        summary += "╚════════════════════════════════════════════╝"
        
        return summary
    
    async def auto_maintenance_check(self) -> Dict:
        """自动维护检查（返回是否需要维护）"""
        report = await self.check_session_health()
        
        needs_maintenance = False
        reasons = []
        
        # 判断是否需要维护
        if report["health_score"] < self.HEALTH_THRESHOLDS["warning"]:
            needs_maintenance = True
            reasons.append("健康评分过低")
        
        if not report["critical_cookies_present"]:
            needs_maintenance = True
            reasons.append("关键Cookie缺失")
        
        if report["expired"]:
            needs_maintenance = True
            reasons.append("存在已过期Cookie")
        
        return {
            "needs_maintenance": needs_maintenance,
            "reasons": reasons,
            "report": report
        }


# ========================================
# 便捷函数
# ========================================

async def quick_health_check(context: BrowserContext, platform: str = "xiaohongshu") -> None:
    """
    快速健康检查并打印报告
    
    Args:
        context: Playwright浏览器上下文
        platform: 平台名称
    
    示例:
        await quick_health_check(context, "xiaohongshu")
    """
    monitor = SessionHealthMonitor(context, platform)
    await monitor.check_session_health()
    print(monitor.get_health_summary())


if __name__ == "__main__":
    print("🩺 Session健康监控系统已就绪")
    print("="*60)
    print("功能：")
    print("  • Cookie有效期监控")
    print("  • Session活跃度检测")
    print("  • 登录状态验证")
    print("  • 自动维护建议")
    print("  • 健康评分系统 (0-100)")
    print("="*60)
