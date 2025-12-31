# 🚀 系统快速启动指南

**系统状态**: ✅ **完全就绪**  
**最后更新**: 2025年12月31日  

---

## ⚡ 快速开始 (3步)

### 步骤 1️⃣ - 启动菜单
```bash
python START.py
```

### 步骤 2️⃣ - 首次登录 (仅需一次)
选择菜单选项 **[2]** - 🔐 登录账号
```bash
# 系统会启动 Microsoft Edge 浏览器
# 手动登录小红书和闲鱼
# 登录信息自动保存到 browser_profile/ 目录
```

### 步骤 3️⃣ - 开始爬虫
选择菜单选项 **[3]** - 🤖 完全自动爬虫
```bash
# 系统自动使用已保存的登录状态
# 爬取最新数据并分析
# 推送结果到企业微信
```

---

## 📋 菜单选项速览

| 选项 | 功能 | 耗时 | 场景 |
|------|------|------|------|
| **[1]** | 快速测试（离线演示） | <1秒 | 验证系统是否正常工作 |
| **[2]** | 登录账号（手动登录） | 1-5分钟 | 首次设置，保存登录状态 |
| **[3]** | 完全自动爬虫 | 5-10分钟 | 实际数据爬取和分析 |
| **[4]** | 定时调度（后台运行） | 持续运行 | 每天自动运行（09:30, 14:00, 21:30） |
| **[5]** | 系统检查 | <1秒 | 验证环境配置是否正确 |
| **[6]** | 查看文档 | - | 阅读使用指南 |
| **[7]** | 检查依赖 | 1-2分钟 | 安装或更新 Python 包 |
| **[8]** | 测试登录系统 | <1分钟 | 验证持久化登录功能 |
| **[0]** | 退出 | - | 关闭程序 |

---

## 🎯 核心脚本说明

### 主程序
```
START.py              # 中心菜单，所有功能入口
├── main.py          # 完整爬虫 + 分析 + 推送
├── login_helper.py  # 人工登录并保存状态
├── niche_finder.py  # 离线分析演示
└── scheduler.py     # 定时后台运行
```

### 爬虫模块
```
scrapers/
├── spider.py        # 核心爬虫
│   ├── XhsSpider    # 小红书爬虫
│   └── FishSpider   # 闲鱼爬虫
└── advanced_config.py # 高级配置
```

### 分析与推送
```
engine/
└── analyzer.py      # 蓝海指数计算

utils/
└── logic.py         # 企业微信推送
```

### 测试与检查
```
test_persistent_login.py # 登录系统测试
check_system.py          # 环境检查
```

---

## 🔑 关键配置文件

### [config.py](config.py)
```python
EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
USER_DATA_PATH = r"./browser_profile"  # 登录状态保存目录
WECOM_WEBHOOK = "..."                  # 企业微信机器人
MIN_POTENTIAL_SCORE = 120              # 蓝海指数阈值
MAX_COMPETITION = 300                  # 竞争度阈值
```

### [requirements.txt](requirements.txt)
```
playwright>=1.40.0          # 浏览器自动化
playwright-stealth>=1.0     # 反检测补丁
requests                    # HTTP 请求
schedule                    # 定时任务
```

---

## 💾 数据存储

```
browser_profile/        # Edge 浏览器数据 (登录状态, Cookie等)
├── ...               # 浏览器配置文件（自动生成）
└── ...

xhs_data.json          # 小红书示例数据
fish_data.json         # 闲鱼示例数据  
niche_report.json      # 蓝海分析报告示例
```

---

## ✨ 核心特性

### ✅ 持久化登录
- 首次手动登录一次，自动保存状态
- 之后自动使用保存的 Cookie 和 Session
- 支持多账号管理（在 browser_profile 中）

### ✅ 反爬虫检测
- Playwright Stealth 自动注入反检测补丁
- 模拟真实用户行为（延迟、鼠标移动、滚动等）
- WebGL/Canvas 指纹伪装

### ✅ Edge 浏览器专用
- Chromium 内核，比 Chrome 更轻量
- 与 Chrome 完全兼容的 API
- 更稳定的性能

### ✅ 企业微信推送
- 实时推送分析结果
- 美观的消息格式
- 支持定时批量推送

### ✅ 蓝海指数计算
- 综合评分：热度 + 竞争度 + 平均成交
- 自动判断是否推送
- 详细的分析报告

---

## 🔍 常见问题

### Q1: 第一次运行出现 Edge 浏览器未找到错误
**A:** 确保系统已安装 Microsoft Edge 浏览器  
检查路径: `C:\Program Files\Microsoft\Edge\Application\msedge.exe`

### Q2: 登录后仍要求重新登录
**A:** 清除 `browser_profile/` 目录，重新登录  
```bash
rmdir /s /q browser_profile
```

### Q3: 企业微信推送不成功
**A:** 检查 config.py 中的 WECOM_WEBHOOK 是否正确

### Q4: 爬虫速度很慢
**A:** 这是反爬虫机制的设计，故意加入延迟以模拟真实用户

### Q5: 定时任务没有执行
**A:** 确保 Python 进程一直在运行  
建议使用 Windows 任务计划程序定时启动 `python scheduler.py`

---

## 📚 完整文档

| 文档 | 内容 |
|------|------|
| [README.md](README.md) | 项目完整说明 |
| [QUICKSTART.md](QUICKSTART.md) | 快速入门 |
| [PERSISTENT_LOGIN_GUIDE.md](PERSISTENT_LOGIN_GUIDE.md) | 登录系统详解 |
| [EDGE_MIGRATION_COMPLETE.md](EDGE_MIGRATION_COMPLETE.md) | Edge 迁移报告 |
| [CLEANUP_REPORT.md](CLEANUP_REPORT.md) | 系统清理报告 |

---

## 🛠️ 故障排查

### 运行系统检查
```bash
python check_system.py
```
会检查：
- ✅ 所有必要文件是否存在
- ✅ 配置文件是否有效
- ✅ Python 依赖是否齐全
- ✅ 模块导入是否正常
- ✅ 登录系统是否工作

### 测试登录系统
```bash
python test_persistent_login.py
```
会验证：
- ✅ 浏览器是否正常启动
- ✅ 反检测补丁是否有效
- ✅ 持久化数据是否正确保存
- ✅ 人类行为模拟是否正常

---

## 📞 快速命令参考

```bash
# 启动菜单（推荐）
python START.py

# 直接运行各个脚本
python main.py                  # 完全自动爬虫
python login_helper.py          # 手动登录
python niche_finder.py          # 离线演示
python scheduler.py             # 定时调度
python check_system.py          # 系统检查
python test_persistent_login.py # 登录测试

# 安装依赖
pip install -r requirements.txt

# 更新依赖
pip install --upgrade -r requirements.txt
```

---

## ⚡ 性能提示

- 首次爬虫会比较慢（10-15分钟），这是反爬虫机制
- 之后爬虫会更快（5-10分钟）
- 定时任务运行不会阻塞其他程序
- 系统占用内存约 200-300 MB

---

**系统已完全优化、清理和验证！准备好开始了吗？** 🚀

现在运行: `python START.py`

