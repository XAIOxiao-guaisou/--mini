# 📑 快速导航索引

## 🎯 我需要...

### 🚀 快速开始
- **5 分钟快速开始** → [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md)
- **运行主程序** → `python main.py`
- **完整验证系统** → `python tests/final_verification.py`

### 📚 了解项目
- **项目总览** → [PROJECT_README.md](PROJECT_README.md)
- **项目结构详解** → [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
- **修复总结（最详细）** → [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md)

### 🐛 解决问题

#### 数据提取问题
- "为什么返回 0 条数据？" → [docs/fixes/DATA_EXTRACTION_FIX.md](docs/fixes/DATA_EXTRACTION_FIX.md)
- "如何改进数据提取？" → [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md#修复-3-数据提取选择器和逻辑)

#### 登录问题
- "登录状态怎么持久化？" → [docs/guides/PERSISTENT_LOGIN_GUIDE.md](docs/guides/PERSISTENT_LOGIN_GUIDE.md)
- "登录失败怎么办？" → [docs/fixes/PERSISTENT_LOGIN_FIX.md](docs/fixes/PERSISTENT_LOGIN_FIX.md)

#### 浏览器问题
- "Edge 浏览器如何配置？" → [docs/fixes/EDGE_MIGRATION_COMPLETE.md](docs/fixes/EDGE_MIGRATION_COMPLETE.md)
- "Stealth 反检测问题？" → [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md#修复-1-导入和-stealth-应用)

### 🧪 运行测试

| 测试 | 命令 | 说明 |
|------|------|------|
| **最终验证** | `python tests/final_verification.py` | 完整验证，推荐 ⭐ |
| **完整流程** | `python tests/test_full_pipeline.py` | 端到端测试 |
| **数据提取** | `python tests/test_extraction_fix.py` | 提取功能验证 |
| **登录持久化** | `python tests/test_persistent_login.py` | 登录功能验证 |

### 🔧 调试和诊断

| 任务 | 脚本 | 用途 |
|------|------|------|
| 调试数据提取 | `python temp/debug_xhs_scraping.py` | 诊断爬虫问题 |
| 调试登录 | `python temp/debug_persistent_login.py` | 诊断登录问题 |
| 验证修复 | `python temp/verify_fix.py` | 检查修复状态 |

### 📖 查看代码

| 想了解 | 文件 | 行号 |
|--------|------|------|
| 爬虫主类 | `scrapers/spider.py` | 全文 (1,350行) |
| Stealth 应用 | `scrapers/spider.py` | 184-190 |
| 数据提取 | `scrapers/spider.py` | 561-655 |
| API 调用 | `scrapers/spider.py` | 509-560 |
| 登录检查 | `scrapers/spider.py` | 255-305 |

### 📊 查看数据

| 数据 | 位置 |
|------|------|
| 小红书爬取结果 | `xhs_data.json` |
| 闲鱼爬取结果 | `fish_data.json` |
| 细分市场报告 | `niche_report.json` |
| 系统日志 | `niche_finder.log` |

### ⚙️ 修改配置

| 配置 | 文件 | 修改方法 |
|------|------|---------|
| 爬虫参数 | `config.py` | 编辑配置值 |
| 请求头 | `scrapers/spider.py` | HeaderBuilder 类 |
| 选择器 | `scrapers/spider.py` | _try_page_scraping 方法 |
| 延迟时间 | `scrapers/spider.py` | delay_manager 对象 |

---

## 📂 文件树速查

```
iostoupin/
│
├── 🚀 main.py                    # 主程序 - 日常运行
├── 🔐 login_helper.py            # 登录助手 - 首次登录
├── ⚙️  config.py                 # 配置文件 - 修改参数
│
├── 📂 scrapers/
│   └── spider.py                 # 爬虫核心 (1,350 行)
│
├── 📂 docs/
│   ├── guides/
│   │   ├── QUICKSTART.md         # 5 分钟快速开始
│   │   ├── PERSISTENT_LOGIN_GUIDE.md  # 登录详解
│   │   └── QUICKSTART.py         # 示例代码
│   │
│   └── fixes/
│       ├── FINAL_SUMMARY.md      # 完整修复总结
│       ├── DATA_EXTRACTION_FIX.md # 数据提取修复
│       ├── PERSISTENT_LOGIN_FIX.md # 登录修复
│       └── EDGE_MIGRATION_COMPLETE.md
│
├── 🧪 tests/
│   ├── final_verification.py     # 最终验证 ⭐
│   ├── test_full_pipeline.py     # 完整流程
│   ├── test_extraction_fix.py    # 数据提取验证
│   │
│   └── fixtures/
│       ├── xhs_page.html         # 页面样本
│       └── xhs_api_response.json # API 样本
│
├── 🔧 temp/
│   ├── debug_xhs_scraping.py     # 爬虫调试
│   ├── debug_persistent_login.py # 登录调试
│   └── verify_fix.py             # 修复验证
│
└── 💾 browser_profile/           # 浏览器数据 (96.7MB)
```

---

## 🎓 学习路径

### 第一次使用（15 分钟）
1. 阅读: [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md)
2. 运行: `python login_helper.py`
3. 验证: `python tests/final_verification.py`

### 深入了解（30 分钟）
1. 阅读: [PROJECT_README.md](PROJECT_README.md)
2. 查看: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
3. 检查: `scrapers/spider.py` 核心类

### 完全掌握（1-2 小时）
1. 学习: [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md)
2. 理解: 所有 4 个修复点
3. 运行: 所有测试脚本
4. 尝试: 修改配置并爬取数据

### 二次开发（2+ 小时）
1. 研究: `scrapers/spider.py` 全文
2. 分析: DOM 选择器策略
3. 学习: JavaScript 评估提取
4. 扩展: 添加新的爬虫或分析功能

---

## ❓ 常见问题速查

| Q | A | 链接 |
|---|---|------|
| 怎么快速开始？ | 运行 QUICKSTART.md | [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md) |
| 为什么返回 0 条数据？ | 选择器不匹配（已修复）| [docs/fixes/DATA_EXTRACTION_FIX.md](docs/fixes/DATA_EXTRACTION_FIX.md) |
| 登录状态如何保留？ | browser_profile 缓存 | [docs/guides/PERSISTENT_LOGIN_GUIDE.md](docs/guides/PERSISTENT_LOGIN_GUIDE.md) |
| 如何手动登录？ | 运行 login_helper.py | [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md) |
| Stealth 反检测？ | await Stealth().apply_stealth_async() | [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md) |
| 如何验证修复？ | 运行 tests/final_verification.py | [README](PROJECT_README.md) |
| 项目结构是什么？ | 详见 PROJECT_STRUCTURE.md | [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) |
| 如何调试问题？ | 运行 temp/ 中的脚本 | [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md#-temp--临时和调试文件) |

---

## 🔗 直接链接

### 核心文档
- [PROJECT_README.md](PROJECT_README.md) - 项目总览
- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - 项目结构详解
- [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md) - 快速开始

### 修复文档
- [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md) - 完整修复总结
- [docs/fixes/DATA_EXTRACTION_FIX.md](docs/fixes/DATA_EXTRACTION_FIX.md) - 数据提取修复
- [docs/fixes/PERSISTENT_LOGIN_FIX.md](docs/fixes/PERSISTENT_LOGIN_FIX.md) - 登录修复

### 指南文档
- [docs/guides/PERSISTENT_LOGIN_GUIDE.md](docs/guides/PERSISTENT_LOGIN_GUIDE.md) - 登录指南
- [docs/guides/QUICKSTART.py](docs/guides/QUICKSTART.py) - 示例代码

### 测试脚本
- [tests/final_verification.py](tests/final_verification.py) - 最终验证
- [tests/test_full_pipeline.py](tests/test_full_pipeline.py) - 完整流程
- [tests/test_extraction_fix.py](tests/test_extraction_fix.py) - 数据提取验证

---

## 📞 支持信息

### 运行诊断
```bash
# 完整验证（推荐）
python tests/final_verification.py

# 或快速诊断
python temp/verify_fix.py
```

### 查看日志
```bash
# 查看最新日志
Get-Content niche_finder.log -Tail 50

# 或查看所有日志
Get-Content niche_finder.log
```

### 重置系统
```bash
# 删除浏览器数据（需要重新登录）
rmdir /s /q browser_profile

# 删除临时数据
del *.json

# 重新启动
python login_helper.py
```

---

## 🎯 推荐查阅顺序

**初学者** (第一次使用):
1. [PROJECT_README.md](PROJECT_README.md) - 5 分钟了解项目
2. [docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md) - 5 分钟快速开始
3. 运行 `python login_helper.py` 并验证

**开发者** (需要修改代码):
1. [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - 了解架构
2. [docs/fixes/FINAL_SUMMARY.md](docs/fixes/FINAL_SUMMARY.md) - 了解修复
3. `scrapers/spider.py` - 阅读源代码

**故障排查** (遇到问题):
1. 运行 `python tests/final_verification.py` - 自动诊断
2. 查看 [PROJECT_README.md](PROJECT_README.md#-故障排查) - 常见问题
3. 查看相关修复文档 - 获取解决方案

---

## ✨ 快捷命令

```bash
# 【最常用】运行主程序
python main.py

# 【首次】手动登录
python login_helper.py

# 【验证】完整系统检查
python tests/final_verification.py

# 【调试】爬虫问题诊断
python temp/debug_xhs_scraping.py

# 【调试】登录问题诊断
python temp/debug_persistent_login.py

# 【数据】查看爬取结果
cat xhs_data.json | python -m json.tool | more

# 【查看】系统日志
Get-Content niche_finder.log -Tail 100
```

---

**提示**: 本文件是项目导航中心。如果您不确定在哪里找某个文件或文档，先查看这里！

**最后更新**: 2024年 | **版本**: 2.0 | **状态**: ✅ 完全就绪
