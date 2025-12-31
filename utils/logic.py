"""
蓝海推送逻辑模块
处理企业微信推送和数据分析流程解耦
"""

import requests
from typing import Dict, Optional
from config import WECOM_WEBHOOK, MIN_POTENTIAL_SCORE, MAX_COMPETITION


class NichePushLogic:
    """蓝海推送逻辑处理器"""
    
    def __init__(self, webhook_url: str = WECOM_WEBHOOK):
        """
        初始化推送器
        
        Args:
            webhook_url: 企业微信Webhook地址
        """
        self.webhook_url = webhook_url
        self.push_count = 0
    
    def push_to_wecom(
        self,
        keyword: str,
        score: float,
        fish_count: int,
        avg_wants: float,
        suggest_title: str = "",
        xhs_heat: int = 0
    ) -> bool:
        """
        推送蓝海词条到企业微信
        
        消息格式：
        ```
        🚀 发现高潜蓝海词: {keyword}
        
        潜力指数: {score}
        市场竞争: 仅 {fish_count} 个卖家
        用户需求: 平均 {avg_wants} 人想要
        
        💡 建议行动
        [复制文案] {suggest_title}
        ```
        
        Args:
            keyword: 关键词
            score: 蓝海指数
            fish_count: 闲鱼商品数
            avg_wants: 平均想要人数
            suggest_title: 建议文案标题
            xhs_heat: 小红书热度
            
        Returns:
            是否发送成功
        """
        
        # 检查是否符合推送条件
        if score < MIN_POTENTIAL_SCORE:
            print(f"⚠ 词条 '{keyword}' 蓝海指数 {score} 低于阈值 {MIN_POTENTIAL_SCORE}，跳过推送")
            return False
        
        if fish_count > MAX_COMPETITION:
            print(f"⚠ 词条 '{keyword}' 竞争度 {fish_count} 超过阈值 {MAX_COMPETITION}，跳过推送")
            return False
        
        # 构建Markdown消息
        markdown_content = self._format_message(
            keyword=keyword,
            score=score,
            fish_count=fish_count,
            avg_wants=avg_wants,
            suggest_title=suggest_title,
            xhs_heat=xhs_heat
        )
        
        # 发送到企业微信
        return self._send_to_wecom(markdown_content)
    
    def _format_message(
        self,
        keyword: str,
        score: float,
        fish_count: int,
        avg_wants: float,
        suggest_title: str = "",
        xhs_heat: int = 0
    ) -> str:
        """
        格式化推送消息
        
        Args:
            keyword: 关键词
            score: 蓝海指数
            fish_count: 竞争对手数
            avg_wants: 平均想要人数
            suggest_title: 建议文案
            xhs_heat: 小红书热度
            
        Returns:
            Markdown格式的消息
        """
        
        # 确定评级
        if score >= 1000:
            rating = "⭐⭐⭐⭐⭐ 顶级蓝海"
            emoji = "🚀"
        elif score >= 500:
            rating = "⭐⭐⭐⭐ 优质蓝海"
            emoji = "🌟"
        else:
            rating = "⭐⭐⭐ 良好蓝海"
            emoji = "💎"
        
        # 构建消息
        message_lines = [
            f"{emoji} **发现高潜蓝海词条：{keyword}**",
            "",
            "**📊 潜力指数**",
            f"> <font color=\"warning\">{score:.2f}</font>（{rating}）",
            "",
            "**🎯 市场情况**",
            f"> • 小红书热度：<font color=\"info\">{xhs_heat:,}</font>",
            f"> • 闲鱼竞争：<font color=\"info\">仅 {fish_count} 个卖家</font>",
            f"> • 用户需求：<font color=\"info\">平均 {avg_wants:.1f} 人想要</font>",
            ""
        ]
        
        # 添加建议
        if suggest_title:
            message_lines.extend([
                "**💡 建议行动**",
                f"> 📝 **建议文案标题**",
                f"> {suggest_title}",
                ""
            ])
        
        message_lines.extend([
            "---",
            "**⏰ 时机提示**",
            "> • 发现时间：即刻推送",
            "> • 建议策略：快速上架，抢占市场先机",
            "> • 预期周期：7-14 天内见效"
        ])
        
        return "\n".join(message_lines)
    
    def _send_to_wecom(self, content: str) -> bool:
        """
        发送Markdown消息到企业微信
        
        Args:
            content: Markdown格式的消息内容
            
        Returns:
            是否发送成功
        """
        
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        try:
            print(f"📤 正在推送到企业微信...")
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10,
                proxies={}  # 禁用代理，直接连接
            )
            
            result = response.json()
            
            if result.get('errcode') == 0:
                self.push_count += 1
                print(f"✅ 已推送蓝海词条（累计：{self.push_count}个）")
                return True
            else:
                error_msg = result.get('errmsg', '未知错误')
                print(f"❌ 企业微信推送失败：{error_msg}")
                return False
        
        except requests.exceptions.Timeout:
            print("❌ 推送请求超时")
            return False
        except Exception as e:
            print(f"❌ 推送异常：{e}")
            return False
    
    def batch_push(self, results: list) -> int:
        """
        批量推送多个蓝海词条
        
        Args:
            results: 分析结果列表
            
        Returns:
            成功推送的个数
        """
        success_count = 0
        
        for item in results:
            # 提取参数
            keyword = item.get('词条', '')
            score = item.get('蓝海指数', 0)
            fish_count = item.get('闲鱼商品数', 0)
            avg_wants = item.get('平均想要数', 0)
            xhs_heat = item.get('小红书热度', 0)
            
            # 推送
            if self.push_to_wecom(
                keyword=keyword,
                score=score,
                fish_count=fish_count,
                avg_wants=avg_wants,
                xhs_heat=int(xhs_heat)
            ):
                success_count += 1
        
        return success_count


def push_to_wecom(
    keyword: str,
    score: float,
    fish_count: int,
    avg_wants: float,
    suggest_title: str = "",
    xhs_heat: int = 0
) -> bool:
    """便捷函数：推送单个蓝海词条"""
    pusher = NichePushLogic()
    return pusher.push_to_wecom(
        keyword=keyword,
        score=score,
        fish_count=fish_count,
        avg_wants=avg_wants,
        suggest_title=suggest_title,
        xhs_heat=xhs_heat
    )


if __name__ == '__main__':
    # 测试推送功能
    print("="*60)
    print("企业微信推送测试")
    print("="*60)
    
    pusher = NichePushLogic()
    
    # 测试单条推送
    success = pusher.push_to_wecom(
        keyword="复古相机",
        score=2812.5,
        fish_count=80,
        avg_wants=15.0,
        suggest_title="复古胶卷相机 - 2025年必入拍照神器",
        xhs_heat=15000
    )
    
    if success:
        print("\n✅ 推送测试成功！")
    else:
        print("\n❌ 推送测试失败，请检查Webhook地址是否正确")
