# 📂 项目结构说明

## 概览

```
iostoupin/
├── 核心程序文件（根目录）
├── 📂 scrapers/          爬虫核心模块
├── 📂 engine/            数据分析引擎
├── 📂 utils/             工具函数
├── 📂 docs/              📚 文档（按分类）
├── 📂 tests/             🧪 测试脚本
├── 📂 temp/              🔧 临时文件
└── 📂 browser_profile/   💾 浏览器数据缓存
```

---

## 📄 根目录文件

### 主要文件

| 文件 | 说明 | 何时使用 |
|------|------|---------|
| **main.py** | 主程序入口 | 日常运行 |
| **login_helper.py** | 登录助手 | 首次登录或需要重新登录 |
| **config.py** | 配置文件 | 修改爬虫参数 |
| **requirements.txt** | 依赖清单 | 初始化环境 |
| **scheduler.py** | 定时调度器 | 定时爬取任务 |
| **niche_finder.py** | 细分市场分析 | 市场分析功能 |

### 输出文件

| 文件 | 内容 | 更新频率 |
|------|------|---------|
| **xhs_data.json** | 小红书爬取结果 | 每次爬取 |
| **fish_data.json** | 闲鱼爬取结果 | 每次爬取 |
| **niche_report.json** | 细分市场报告 | 每次分析 |
| **niche_finder.log** | 系统日志 | 实时写入 |

---

## 📂 scrapers/ - 爬虫核心模块

```
scrapers/
├── __init__.py
└── spider.py                    (1,350 行)
    ├── HeaderBuilder            请求头生成器
    ├── XhsSpider                小红书爬虫类
    │   ├── init_browser()       浏览器初始化
    │   ├── check_login_status() 登录状态检查
    │   ├── get_xhs_trends()     主爬取方法
    │   ├── _try_api_call()      API 调用
    │   ├── _try_page_scraping() 页面爬取 ✨
    │   └── close()              清理资源
    │
    └── FishSpider               闲鱼爬虫类
        ├── init_browser()
        ├── check_login_status()
        ├── get_fish_trends()
        ├── _try_api_call_fish()
        └── _try_page_scraping_fish()
```

### 核心类说明

#### XhsSpider - 小红书爬虫

```python
# 初始化
spider = XhsSpider(headless=False)
await spider.init_browser()

# 检查登录
is_logged = await spider.check_login_status()

# 爬取数据
results = await spider.get_xhs_trends(['关键词1', '关键词2'])
# returns: {
#     '关键词1': {
#         'count': 10,
#         'trend_score': 6500,
#         'notes': [{title, user, likes}, ...],
#         'source': 'page_scraping'
#     }
# }

# 关闭
await spider.close()
```

#### FishSpider - 闲鱼爬虫

类似接口，用于闲鱼数据爬取

### 关键方法详解

#### `_try_page_scraping()` - 页面爬取 ✨

**之前的问题**:
- 使用通用选择器: `div[class*="note-card"]`
- 不能识别 Vue.js 组件
- 返回 0 条数据 ❌

**现在的解决方案**:
- 使用 Vue.js 选择器: `section[data-v-2acb2abe]`
- JavaScript 评估提取数据
- 返回 10 条数据 ✅

```python
# 执行 JavaScript 提取
result = await self.page.evaluate("""
    () => {
        const notes = [];
        const noteCards = document.querySelectorAll('section[data-v-2acb2abe]');
        
        noteCards.forEach((card) => {
            const title = card.querySelector('.reds-note-title')?.textContent;
            const user = card.querySelector('.reds-note-user')?.getAttribute('name');
            const image = card.querySelector('img[alt]')?.src;
            
            notes.push({title, user, image, likes});
        });
        
        return notes;
    }
""")
```

---

## 📂 engine/ - 数据分析引擎

```
engine/
├── __init__.py
└── analyzer.py
    ├── TrendAnalyzer        趋势分析器
    │   ├── calculate_score()
    │   └── analyze_trend()
    │
    └── ReportGenerator      报告生成器
        ├── generate_report()
        └── export_json()
```

### 使用示例

```python
from engine.analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
score = analyzer.calculate_score(data)
report = analyzer.analyze_trend(scores)
```

---

## 📂 utils/ - 工具函数

```
utils/
├── __init__.py
└── logic.py
    ├── calculate_trend_score()    趋势分数计算
    ├── parse_json()              JSON 解析
    └── format_output()           输出格式化
```

---

## 📂 docs/ - 📚 文档库

### 文件夹结构

```
docs/
├── fixes/                       修复相关文档
│   ├── DATA_EXTRACTION_FIX.md        数据提取修复详解
│   ├── FINAL_SUMMARY.md              完整的技术总结
│   ├── FIX_SUMMARY.md                修复摘要
│   ├── FIX_COMPLETION.md             修复完成报告
│   ├── PERSISTENT_LOGIN_DEBUG.md     登录调试记录
│   ├── PERSISTENT_LOGIN_FIX.md       登录修复指南
│   ├── EDGE_MIGRATION_COMPLETE.md    浏览器迁移指南
│   └── PLAYWRIGHT_MIGRATION.md       Playwright 迁移指南
│
└── guides/                      使用指南
    ├── QUICKSTART.md                 快速开始（5 分钟）
    ├── PERSISTENT_LOGIN_GUIDE.md     登录系统详解
    ├── QUICKSTART.py                 快速开始示例代码
    └── PLAYWRIGHT_QUICKREF.md        Playwright 快速参考
```

### 文档查阅指南

**想快速开始？**
→ [docs/guides/QUICKSTART.md](../docs/guides/QUICKSTART.md)

**遇到数据提取问题？**
→ [docs/fixes/DATA_EXTRACTION_FIX.md](../docs/fixes/DATA_EXTRACTION_FIX.md)

**登录问题？**
→ [docs/guides/PERSISTENT_LOGIN_GUIDE.md](../docs/guides/PERSISTENT_LOGIN_GUIDE.md)

**想了解全部修复？**
→ [docs/fixes/FINAL_SUMMARY.md](../docs/fixes/FINAL_SUMMARY.md)

---

## 🧪 tests/ - 测试脚本

```
tests/
├── final_verification.py          ⭐ 最终验证（推荐）
│   ├── 初始化浏览器
│   ├── 检查登录状态
│   ├── 单关键词爬取测试
│   ├── 多关键词爬取测试
│   └── 系统状态总结
│
├── test_full_pipeline.py          完整流程测试
│   ├── 初始化爬虫
│   ├── 检查登录
│   ├── 执行爬取
│   └── 显示结果
│
├── test_extraction_fix.py         数据提取验证
│   ├── 初始化浏览器
│   ├── 搜索关键词
│   ├── 检查页面内容
│   ├── 执行改进的提取
│   └── 显示结果
│
├── test_persistent_login.py       登录持久化测试
│
└── fixtures/                      测试数据和样本
    ├── xhs_page.html              小红书页面样本（57KB）
    ├── test_page.html             测试页面样本
    └── xhs_api_response.json      API 响应示例
```

### 测试运行指南

```bash
# 1. 最终验证（完整，推荐）
python tests/final_verification.py

# 2. 完整流程测试
python tests/test_full_pipeline.py

# 3. 数据提取验证
python tests/test_extraction_fix.py

# 4. 登录持久化测试
python tests/test_persistent_login.py
```

### 预期输出

✅ 成功时：
```
✨ 最终验证脚本 - 所有修复验证
1️⃣  初始化浏览器... ✅
2️⃣  检查登录状态... ✅ 已登录（Cookies 有效）
3️⃣  单关键词爬取测试
    关键词: 复古相机
    └─ 数据源: page_scraping
    └─ 笔记数: 10 ✅
4️⃣  多关键词爬取测试
    ✅ 胶卷相机: 10 条 (来自 page_scraping)
    ✅ 底片相机: 10 条 (来自 page_scraping)
5️⃣  系统状态总结
    ✔ Stealth API 正确实现
    ✔ 持久化登录正常工作
    ✔ 数据提取改进成功

🎉 所有修复验证成功！系统已准备就绪
```

---

## 🔧 temp/ - 临时和调试文件

```
temp/
├── debug_xhs_scraping.py         小红书爬虫调试脚本
├── debug_persistent_login.py     登录持久化调试
├── verify_fix.py                 修复验证脚本
├── verify_persistent_login.py    登录验证脚本
├── analyze_dom.py                DOM 结构分析
└── check_system.py               系统检查脚本
```

### 调试技巧

```bash
# 调试数据提取问题
python temp/debug_xhs_scraping.py

# 调试登录问题
python temp/debug_persistent_login.py

# 验证修复
python temp/verify_fix.py
```

---

## 💾 browser_profile/ - 浏览器数据缓存

```
browser_profile/
├── Default/                  Edge 的默认配置文件夹
│   ├── Cookies              小红书和闲鱼的 Cookies
│   ├── Local Storage/       LocalStorage 数据
│   ├── Session Storage/     会话数据
│   └── History              浏览历史
│
├── Local State             全局配置
├── Preferences             浏览器偏好设置
└── ...
```

### 重要信息

| 项 | 值 |
|----|-----|
| **大小** | 96.7MB（完整缓存） |
| **内容** | 21+ Cookies + 18+ LocalStorage |
| **用途** | 跨会话复用登录状态 |
| **删除后果** | 丢失登录状态，需要重新登录 |
| **备份建议** | 定期备份以防意外 |

### 备份和恢复

```bash
# 备份浏览器数据
Copy-Item -Path "browser_profile" -Destination "browser_profile.backup" -Recurse

# 恢复备份
Remove-Item -Path "browser_profile" -Recurse
Copy-Item -Path "browser_profile.backup" -Destination "browser_profile" -Recurse
```

---

## 📊 数据输出文件

### xhs_data.json - 小红书数据

```json
{
  "复古相机": {
    "count": 10,
    "trend_score": 6140,
    "notes": [
      {
        "title": "上海街拍！模特教你高级感的密码",
        "user": "张璨CAN",
        "likes": 225,
        "image_url": "https://sns-webpic.xhscdn.com/..."
      },
      ...
    ],
    "source": "page_scraping",
    "timestamp": "2024-12-31T10:30:45"
  }
}
```

### fish_data.json - 闲鱼数据

类似结构，包含闲鱼商品信息

### niche_report.json - 细分市场报告

```json
{
  "analysis_date": "2024-12-31",
  "market_overview": {...},
  "category_analysis": {...},
  "trend_prediction": {...}
}
```

---

## 🎯 工作流程

### 典型使用流程

```
1. 首次使用
   └─ python login_helper.py          手动登录
      └─ browser_profile/ 生成         浏览器数据保存

2. 日常使用
   └─ python main.py                  主程序
      ├─ 选项 [1]: 查看已保存数据
      ├─ 选项 [2]: 爬取闲鱼
      ├─ 选项 [3]: 爬取小红书
      └─ 选项 [0]: 退出

3. 验证系统
   └─ python tests/final_verification.py   全面验证
      ├─ 初始化 ✓
      ├─ 登录检查 ✓
      ├─ 单关键词 ✓
      ├─ 多关键词 ✓
      └─ 系统状态 ✓

4. 定时爬取
   └─ python scheduler.py               后台定时爬取
      ├─ 每小时爬取一次
      ├─ 自动保存数据
      └─ 生成报告
```

---

## 🔍 文件查找速查表

| 需要 | 文件位置 | 备注 |
|------|---------|------|
| 快速开始 | `docs/guides/QUICKSTART.md` | 5 分钟入门 |
| 完整验证 | `tests/final_verification.py` | 推荐运行 |
| 数据提取修复 | `docs/fixes/DATA_EXTRACTION_FIX.md` | 选择器问题 |
| 登录指南 | `docs/guides/PERSISTENT_LOGIN_GUIDE.md` | 登录问题 |
| 爬虫代码 | `scrapers/spider.py` | 核心实现 |
| 测试数据 | `tests/fixtures/` | HTML 样本 |
| 配置修改 | `config.py` | 修改参数 |
| 数据结果 | `xhs_data.json` | 爬取结果 |
| 调试脚本 | `temp/` | 问题诊断 |

---

## 💡 项目整理后的优势

✅ **结构清晰**
- 核心代码与文档分离
- 测试脚本集中管理
- 临时文件不污染根目录

✅ **易于维护**
- 文档分类有序
- 新人快速上手
- 问题诊断方便

✅ **规范化**
- 遵循 Python 项目最佳实践
- 易于扩展和协作
- 便于代码版本管理

✅ **专业化**
- 企业级项目布局
- 完整的文档体系
- 齐全的测试框架

---

## 🚀 后续扩展指南

### 添加新爬虫

```
scrapers/
└── spider.py
    ├── XhsSpider         (现有)
    ├── FishSpider        (现有)
    └── NewPlatformSpider (新增)
        ├── init_browser()
        ├── get_data()
        └── close()
```

### 添加新分析

```
engine/
├── analyzer.py           (现有)
└── new_analyzer.py       (新增)
    ├── CustomAnalyzer
    └── process_data()
```

### 添加新测试

```
tests/
├── final_verification.py (现有)
└── test_new_feature.py   (新增)
    ├── test_xxx()
    └── main()
```

### 添加新文档

```
docs/
├── fixes/               (修复)
├── guides/              (指南)
└── api/                 (新增 - API 文档)
    └── spider_api.md
```

---

**更新时间**: 2024年 | **版本**: 2.0 | **维护者**: 项目开发团队
