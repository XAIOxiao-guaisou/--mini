# 📑 系统文档索引

> 系统已完全优化、清理和验证！所有文档都可在本索引中快速查找。

---

## 🚀 快速开始

**首次使用？从这里开始：**

1. **[QUICK_START.md](QUICK_START.md)** ⭐ - 3分钟快速入门
   - 启动菜单说明
   - 常见问题解答
   - 快速命令参考

2. 运行命令：
   ```bash
   python START.py
   ```

---

## 📚 完整文档

### 核心文档

| 文档 | 描述 | 何时阅读 |
|------|------|--------|
| [README.md](README.md) | 项目完整说明和功能介绍 | 了解整个项目 |
| [QUICKSTART.md](QUICKSTART.md) | 快速启动教程 | 首次使用 |
| [PERSISTENT_LOGIN_GUIDE.md](PERSISTENT_LOGIN_GUIDE.md) | 登录系统详细指南 | 需要深入了解登录机制 |

### 系统报告 (仅供参考)

| 文档 | 描述 | 内容 |
|------|------|------|
| [CLEANUP_REPORT.md](CLEANUP_REPORT.md) | 系统清理报告 | 删除的废旧文件、修复的问题、验证结果 |
| [EDGE_MIGRATION_COMPLETE.md](EDGE_MIGRATION_COMPLETE.md) | Edge 浏览器迁移报告 | 从 Chrome 迁移到 Edge 的所有改动 |

---

## 🎯 按需求查找文档

### "我想快速体验系统"
→ [QUICK_START.md](QUICK_START.md)

### "我想了解登录系统如何工作"
→ [PERSISTENT_LOGIN_GUIDE.md](PERSISTENT_LOGIN_GUIDE.md)

### "我想了解项目完整功能"
→ [README.md](README.md)

### "我想知道系统做了什么优化"
→ [CLEANUP_REPORT.md](CLEANUP_REPORT.md)

### "我想了解 Edge 浏览器的改动"
→ [EDGE_MIGRATION_COMPLETE.md](EDGE_MIGRATION_COMPLETE.md)

### "我需要故障排查"
→ [QUICK_START.md](QUICK_START.md#-常见问题) 或 运行 `python check_system.py`

---

## ⚡ 快速命令

```bash
# 启动菜单（主入口）
python START.py

# 系统检查（诊断问题）
python check_system.py

# 测试登录系统
python test_persistent_login.py

# 查看本索引
# 你正在阅读这个文件！
```

---

## 📊 系统架构概览

```
┌─────────────────────────────────────┐
│      START.py (启动菜单)            │
│     中心控制，所有功能入口           │
└──────────┬──────────────────────────┘
           │
    ┌──────┼──────┬──────┬──────┐
    │      │      │      │      │
    v      v      v      v      v
  [1]    [2]    [3]    [4]    [5]
 快速    登录   完全   定时   系统
 测试    账号   自动   调度   检查
    │      │      │      │      │
    v      v      v      v      v
niche  login  main  sched check_
finder helper.py   uler  system
.py    .py        .py    .py
        │      │    │
        v      v    v
        爬虫模块（scrapers/spider.py）
        ├── XhsSpider    (小红书)
        └── FishSpider   (闲鱼)
        │
        v
        分析与推送
        ├── engine/analyzer.py    (蓝海分析)
        └── utils/logic.py        (微信推送)
```

---

## 🔍 文件说明

### 配置文件
- **[config.py](config.py)** - 全局配置（浏览器路径、微信、阈值等）
- **[requirements.txt](requirements.txt)** - Python 依赖包列表

### 主程序
- **[START.py](START.py)** - 启动菜单（推荐入口）
- **[main.py](main.py)** - 完全自动爬虫
- **[login_helper.py](login_helper.py)** - 人工登录助手
- **[niche_finder.py](niche_finder.py)** - 离线演示
- **[scheduler.py](scheduler.py)** - 定时后台运行

### 爬虫模块
- **[scrapers/spider.py](scrapers/spider.py)** - 核心爬虫（XhsSpider, FishSpider）
- **[scrapers/advanced_config.py](scrapers/advanced_config.py)** - 高级配置

### 工具模块
- **[utils/logic.py](utils/logic.py)** - 企业微信推送逻辑
- **[engine/analyzer.py](engine/analyzer.py)** - 蓝海指数分析引擎

### 测试和检查
- **[test_persistent_login.py](test_persistent_login.py)** - 登录系统测试
- **[check_system.py](check_system.py)** - 环境完整性检查

### 数据文件
- **[xhs_data.json](xhs_data.json)** - 小红书示例数据
- **[fish_data.json](fish_data.json)** - 闲鱼示例数据
- **[niche_report.json](niche_report.json)** - 分析报告示例

### 浏览器数据
- **[browser_profile/](browser_profile/)** - Edge 浏览器数据（自动生成）
  - 包含登录状态、Cookie、Session 等

---

## ✅ 系统检查清单

使用以下命令验证系统状态：

```bash
# 完整系统检查
python check_system.py

# 测试登录系统
python test_persistent_login.py

# 快速功能演示
python niche_finder.py
```

---

## 🎯 核心特性

- ✅ **持久化登录** - 首次登录一次，之后自动复用
- ✅ **反爬虫检测** - Stealth 补丁 + 人类行为模拟
- ✅ **Edge 浏览器** - Chromium 内核，轻量且稳定
- ✅ **企业微信推送** - 实时推送分析结果
- ✅ **蓝海指数** - 智能计算和推荐
- ✅ **定时运行** - 每天自动执行

---

## 📞 需要帮助？

1. **快速问题** → 查看 [QUICK_START.md 的常见问题](QUICK_START.md#-常见问题)
2. **系统故障** → 运行 `python check_system.py`
3. **登录问题** → 查看 [PERSISTENT_LOGIN_GUIDE.md](PERSISTENT_LOGIN_GUIDE.md)
4. **功能说明** → 查看 [README.md](README.md)

---

## 🚀 现在就开始！

```bash
python START.py
```

然后选择：
1. **[2]** - 🔐 首次登录（仅需一次）
2. **[3]** - 🤖 开始自动爬虫

---

**最后更新**: 2025年12月31日  
**系统状态**: ✅ 完全就绪  
**文档版本**: v1.0

