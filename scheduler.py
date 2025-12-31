"""
分时调度器
根据时间表自动执行蓝海赛道挖掘任务（无代理单IP环保模式）
"""

import schedule
import time
import logging
from datetime import datetime
from main import NicheHunterEngine


# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NicheScheduler:
    """蓝海赛道任务调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.engine = NicheHunterEngine()
        self.is_running = False
    
    def job_morning(self):
        """早高峰任务（9:30）"""
        logger.info("⏰ 执行早高峰任务")
        self.engine.run_mission(
            top_trends_n=15,
            top_results_n=5,
            enable_push=True
        )
    
    def job_afternoon(self):
        """午间任务（14:00）"""
        logger.info("⏰ 执行午间任务")
        self.engine.run_mission(
            top_trends_n=15,
            top_results_n=5,
            enable_push=True
        )
    
    def job_evening(self):
        """晚间任务（21:30）"""
        logger.info("⏰ 执行晚间任务")
        self.engine.run_mission(
            top_trends_n=15,
            top_results_n=5,
            enable_push=True
        )
    
    def setup_schedule(self):
        """设置任务日程"""
        print("\n" + "="*60)
        print("📅 蓝海赛道分时调度器")
        print("="*60)
        print("\n已设置以下定时任务：")
        
        # 早高峰（9:30）
        schedule.every().day.at("09:30").do(self.job_morning)
        print("  • 09:30 早高峰扫描（小红书流量活跃）")
        
        # 午间（14:00）
        schedule.every().day.at("14:00").do(self.job_afternoon)
        print("  • 14:00 午间扫描（用户需求高峰）")
        
        # 晚间（21:30）
        schedule.every().day.at("21:30").do(self.job_evening)
        print("  • 21:30 晚间扫描（流量最强期）")
        
        print("\n💡 设计理由：")
        print("  → 避免24小时狂刷，降低被检测风险")
        print("  → 抓取时段与用户活跃时段重合，数据质量高")
        print("  → 三次任务间隔均衡，数据更新及时")
        print("\n" + "="*60 + "\n")
    
    def run(self, test_mode: bool = False):
        """
        启动调度器
        
        Args:
            test_mode: 测试模式（立即执行一次任务）
        """
        self.is_running = True
        self.setup_schedule()
        
        if test_mode:
            print("🧪 测试模式：立即执行一次任务\n")
            self.job_morning()
            print("\n✅ 测试任务完成，正式调度器已启动\n")
        
        logger.info("调度器已启动，等待任务触发...")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            logger.info("调度器已停止")
            self.stop()
    
    def stop(self):
        """停止调度器"""
        self.is_running = False
        logger.info("调度器停止")


def main():
    """主程序"""
    scheduler = NicheScheduler()
    
    # 启动调度器
    # test_mode=True 时会立即执行一次任务作为测试
    scheduler.run(test_mode=False)


if __name__ == '__main__':
    main()
