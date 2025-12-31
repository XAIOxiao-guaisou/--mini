"""
项目配置文件
包含企业微信推送、浏览器配置、算法阈值等参数
"""

# ==================== 企业微信机器人配置 ====================
WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=480bc935-8f0e-4821-bfc6-0e5829781eee"

# ==================== 浏览器配置 ====================
# 浏览器指纹路径，确保单IP环境下Cookie持久化
# 仅使用Edge浏览器（Chromium内核，更稳定）
EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
USER_DATA_PATH = r"./browser_profile"

# ==================== 算法阈值配置 ====================
# 蓝海指数超过多少分才推送
MIN_POTENTIAL_SCORE = 120

# 闲鱼卖家超过此数量则视为红海，不推送
MAX_COMPETITION = 300

# ==================== 数据文件配置 ====================
XHS_DATA_FILE = "xhs_data.json"      # 小红书数据文件
FISH_DATA_FILE = "fish_data.json"    # 闲鱼数据文件
REPORT_FILE = "niche_report.json"    # 分析报告文件

# ==================== 爬虫配置 ====================
REQUEST_TIMEOUT = 30                 # 请求超时时间（秒）
RETRY_TIMES = 3                      # 失败重试次数
DELAY_BETWEEN_REQUESTS = (2, 5)      # 请求间隔时间范围（秒）

# ==================== VPN/代理配置（重要！） ====================
# 禁用代理，直接连接（不走VPN）
DISABLE_PROXY = True                 # 强制禁用代理
USE_DIRECT_CONNECTION = True         # 使用直接连接
PROXY_DICT = {}                      # 空代理字典（不使用任何代理）
NO_PROXY = '*'                       # 所有域名都不使用代理

# ==================== 推送配置 ====================
ENABLE_WECOM_PUSH = True             # 是否启用企业微信推送
TOP_N_RESULTS = 5                    # 推送前N个最佳赛道
PUSH_INTERVAL = 3600                 # 推送间隔（秒），避免频繁打扰

# ==================== 日志配置 ====================
LOG_LEVEL = "INFO"                   # 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_FILE = "niche_finder.log"        # 日志文件路径
