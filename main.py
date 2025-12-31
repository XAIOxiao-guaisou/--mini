"""
全自动蓝海赛道挖掘主程序
集成爬虫、分析、推送全流程
"""

import time
import random
import json
import logging
from datetime import datetime
from typing import List, Dict
from pathlib import Path

from scrapers.spider import get_xhs_trends, get_fish_data
from engine.analyzer import BlueOceanAnalyzer
from utils.logic import NichePushLogic
from config import (
    DELAY_BETWEEN_REQUESTS, 
    PUSH_INTERVAL,
    LOG_LEVEL,
    LOG_FILE,
    REPORT_FILE,
    ENABLE_WECOM_PUSH,
    MIN_POTENTIAL_SCORE,
    MAX_COMPETITION,
    XHS_DATA_FILE
)


# ==================== 日志配置 ====================
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NicheHunterEngine:
    """蓝海赛道猎人引擎"""
    
    def __init__(self):
        """初始化引擎"""
        self.pusher = NichePushLogic() if ENABLE_WECOM_PUSH else None
        self.results = []
        self.push_records = []
        
    def run_mission(
        self,
        top_trends_n: int = 15,
        top_results_n: int = 5,
        enable_push: bool = ENABLE_WECOM_PUSH
    ) -> Dict:
        """
        执行完整蓝海挖掘任务
        
        流程：
        1. 🔍 抓取小红书热搜词条（前15个）
        2. 🛍️ 查询闲鱼数据（每个词间隔20-30秒）
        3. 📊 计算蓝海指数并排序
        4. 📤 推送符合条件的词条到企业微信
        5. 💾 保存分析报告
        
        Args:
            top_trends_n: 抓取的热搜词条数量
            top_results_n: 返回的最佳赛道数
            enable_push: 是否推送到企业微信
            
        Returns:
            执行结果字典
        """
        
        print("\n" + "="*70)
        print("🚀 启动全网蓝海赛道情报扫描")
        print("="*70)
        
        start_time = datetime.now()
        logger.info("任务开始")
        
        try:
            # 1️⃣ 第一步：抓取小红书热搜词条
            print("\n【第1步】🔍 抓取小红书热搜词条...")
            keywords = self._fetch_xhs_trends(top_trends_n)
            
            if not keywords:
                logger.warning("未能成功获取热搜词条")
                return {
                    'status': 'failed',
                    'message': '未能获取热搜词条',
                    'duration': str(datetime.now() - start_time)
                }
            
            print(f"✓ 成功获取 {len(keywords)} 个热搜词条\n")
            
            # 2️⃣ 第二步：查询闲鱼数据并计算指数
            print("【第2步】🛍️ 查询闲鱼数据并计算蓝海指数...")
            self.results = self._analyze_keywords(keywords)
            
            if not self.results:
                logger.warning("未能分析任何词条")
                return {
                    'status': 'partial_failed',
                    'message': '数据分析失败',
                    'duration': str(datetime.now() - start_time)
                }
            
            # 3️⃣ 第三步：排序并筛选
            print("\n【第3步】📊 筛选优质蓝海词条...")
            top_results = BlueOceanAnalyzer.rank_results(self.results, top_results_n)
            
            # 过滤符合推送条件的词条
            qualified_results = [
                r for r in top_results 
                if BlueOceanAnalyzer.is_qualified(r['蓝海指数'], r['闲鱼商品数'])
            ]
            
            print(f"✓ 发现 {len(qualified_results)} 个优质蓝海词条")
            
            # 打印前5个结果
            print("\n" + "-"*70)
            print("🏆 TOP 5 潜力赛道")
            print("-"*70)
            for i, result in enumerate(top_results[:5], 1):
                self._print_result(i, result)
            
            # 4️⃣ 第四步：推送到企业微信
            if enable_push and qualified_results:
                print("\n【第4步】📤 推送蓝海词条到企业微信...")
                self._push_results(qualified_results)
            
            # 5️⃣ 第五步：保存报告
            print("\n【第5步】💾 保存分析报告...")
            self._save_report(top_results)
            
            # 计算执行时间
            duration = datetime.now() - start_time
            
            print("\n" + "="*70)
            print("✅ 任务完成")
            print("="*70)
            print(f"📊 统计信息：")
            print(f"  • 处理词条：{len(self.results)} 个")
            print(f"  • 优质词条：{len(qualified_results)} 个")
            print(f"  • 推送成功：{len(self.push_records)} 个")
            print(f"  • 执行耗时：{duration}")
            
            logger.info(f"任务成功完成，耗时 {duration}")
            
            return {
                'status': 'success',
                'keywords_analyzed': len(self.results),
                'qualified_keywords': len(qualified_results),
                'push_count': len(self.push_records),
                'top_results': top_results,
                'duration': str(duration)
            }
        
        except Exception as e:
            logger.error(f"任务执行出错：{e}", exc_info=True)
            return {
                'status': 'error',
                'message': str(e),
                'duration': str(datetime.now() - start_time)
            }
    
    def _fetch_xhs_trends(self, top_n: int = 15) -> List[Dict]:
        """
        获取小红书热搜词条
        
        流程：
        1. 从 xhs_data.json 读取初始关键词列表
        2. 使用 Playwright 爬虫获取这些关键词的热搜数据
        3. 返回前 N 个热搜词条
        
        Args:
            top_n: 获取前N个热搜
            
        Returns:
            热搜词条列表
        """
        try:
            # 步骤1：从 xhs_data.json 读取初始关键词
            print("📖 正在加载初始关键词列表...")
            
            xhs_file = Path(XHS_DATA_FILE)
            if not xhs_file.exists():
                logger.error(f"文件不存在：{XHS_DATA_FILE}")
                print(f"❌ 找不到文件：{XHS_DATA_FILE}")
                return []
            
            with open(xhs_file, 'r', encoding='utf-8') as f:
                xhs_data = json.load(f)
            
            # 转换数据格式：从 {keyword: {热度: value}} 转为 [{word: keyword, heat: value}, ...]
            keywords_list = [
                {
                    'word': keyword,
                    'heat': data.get('热度', 0)
                }
                for keyword, data in xhs_data.items()
            ]
            
            if not keywords_list:
                logger.warning("xhs_data.json 中没有有效数据")
                print("❌ xhs_data.json 中没有有效数据")
                return []
            
            print(f"✓ 已加载 {len(keywords_list)} 个初始关键词")
            
            # 步骤2：使用 Playwright 爬虫获取热搜数据
            print("🚀 启动 Playwright 爬虫获取热搜数据...")
            
            # 提取关键词文本列表用于爬虫
            keyword_texts = [item['word'] for item in keywords_list[:top_n]]
            
            try:
                # 调用 Playwright 爬虫
                trends_data = get_xhs_trends(keyword_texts)
                
                # 合并结果：使用爬虫获取的热搜数据，如果爬虫失败则使用本地数据
                result_trends = []
                for item in keywords_list[:top_n]:
                    keyword = item['word']
                    if keyword in trends_data:
                        # 使用爬虫数据
                        result_trends.append({
                            'word': keyword,
                            'heat': trends_data[keyword].get('trend_score', item['heat']),
                            'note_count': trends_data[keyword].get('count', 0),
                            'source': 'crawler'
                        })
                    else:
                        # 降级使用本地数据
                        result_trends.append({
                            'word': keyword,
                            'heat': item['heat'],
                            'note_count': 0,
                            'source': 'local'
                        })
                
                print(f"✓ 成功获取 {len(result_trends)} 个热搜词条")
                logger.info(f"获取热搜词条成功：{len(result_trends)} 个")
                
                return result_trends
            
            except ImportError as e:
                # Playwright 未安装，使用本地数据
                logger.warning(f"Playwright 不可用，使用本地数据：{e}")
                print(f"⚠️  Playwright 不可用，使用本地缓存数据")
                print(f"   请运行：pip install playwright playwright-stealth")
                
                return keywords_list[:top_n]
        
        except Exception as e:
            logger.error(f"获取热搜词条失败：{e}", exc_info=True)
            print(f"❌ 获取热搜词条失败：{e}")
            return []
    
    def _analyze_keywords(self, keywords: List[Dict]) -> List[Dict]:
        """
        分析关键词的蓝海指数
        
        Args:
            keywords: 热搜词条列表
            
        Returns:
            分析结果列表
        """
        results = []
        total = len(keywords)
        
        for idx, keyword_item in enumerate(keywords, 1):
            keyword = keyword_item.get('word', '')
            xhs_heat = keyword_item.get('heat', 0)
            
            if not keyword:
                continue
            
            print(f"\n[{idx}/{total}] 正在分析：{keyword}")
            
            try:
                # 查询闲鱼数据（需要传递列表）
                fish_info = get_fish_data([keyword])
                
                # 计算蓝海指数
                index, analysis = BlueOceanAnalyzer.calculate_detailed_index(
                    xhs_data={'word': keyword, 'heat': xhs_heat},
                    fish_data=fish_info
                )
                
                results.append(analysis)
                
                # 强制冷却（防止IP封禁）
                wait_time = random.uniform(*DELAY_BETWEEN_REQUESTS)
                print(f"⏳ 冷却 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
            
            except ImportError as e:
                # Playwright 未安装
                logger.warning(f"Playwright 不可用，跳过关键词 '{keyword}'：{e}")
                print(f"⚠️  Playwright 不可用，使用本地数据分析")
                
                # 尝试从本地数据中获取闲鱼数据
                try:
                    fish_file = Path('fish_data.json')
                    if fish_file.exists():
                        with open(fish_file, 'r', encoding='utf-8') as f:
                            fish_data_dict = json.load(f)
                        
                        fish_info = fish_data_dict.get(keyword, {
                            '商品数': 0,
                            '想要人数': 0
                        })
                        
                        index, analysis = BlueOceanAnalyzer.calculate_detailed_index(
                            xhs_data={'word': keyword, 'heat': xhs_heat},
                            fish_data=fish_info
                        )
                        results.append(analysis)
                except Exception as local_e:
                    logger.warning(f"使用本地数据分析失败：{local_e}")
                    continue
            
            except Exception as e:
                logger.warning(f"分析词条 '{keyword}' 失败：{e}")
                continue
        
        return results
    
    def _print_result(self, rank: int, result: Dict) -> None:
        """
        打印单个分析结果
        
        Args:
            rank: 排名
            result: 分析结果
        """
        print(f"\n第 {rank} 名：{result['词条']}")
        print(f"  🔥 蓝海指数：{result['蓝海指数']} {result['评级']}")
        print(f"  📈 小红书热度：{result['小红书热度']:,.0f} {result['热度评估']}")
        print(f"  🛍️ 竞争对手：{result['闲鱼商品数']} {result['竞争度评估']}")
        print(f"  ❤️ 平均想要数：{result['平均想要数']:.1f} 人")
    
    def _push_results(self, results: List[Dict]) -> None:
        """
        推送结果到企业微信
        
        Args:
            results: 要推送的结果列表
        """
        if not self.pusher or not results:
            return
        
        success_count = 0
        
        for result in results:
            success = self.pusher.push_to_wecom(
                keyword=result['词条'],
                score=result['蓝海指数'],
                fish_count=result['闲鱼商品数'],
                avg_wants=result['平均想要数'],
                xhs_heat=int(result['小红书热度'])
            )
            
            if success:
                success_count += 1
                self.push_records.append({
                    'keyword': result['词条'],
                    'timestamp': datetime.now().isoformat()
                })
            
            # 推送之间的间隔
            time.sleep(2)
        
        print(f"✓ 推送完成：{success_count}/{len(results)} 成功")
    
    def _save_report(self, results: List[Dict]) -> None:
        """
        保存分析报告
        
        Args:
            results: 分析结果列表
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(self.results),
            'top_results': results,
            'push_records': self.push_records,
            'config': {
                'min_potential_score': MIN_POTENTIAL_SCORE,
                'max_competition': MAX_COMPETITION
            }
        }
        
        try:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            logger.info(f"报告已保存到 {REPORT_FILE}")
            print(f"✓ 报告已保存到：{REPORT_FILE}")
        except Exception as e:
            logger.error(f"保存报告失败：{e}")


def main():
    """主程序入口"""
    
    # 创建引擎实例
    engine = NicheHunterEngine()
    
    # 执行任务
    result = engine.run_mission(
        top_trends_n=15,      # 抓取前15个热搜
        top_results_n=5,      # 返回前5个最佳赛道
        enable_push=ENABLE_WECOM_PUSH  # 是否推送到企业微信
    )
    
    return result


if __name__ == '__main__':
    main()
