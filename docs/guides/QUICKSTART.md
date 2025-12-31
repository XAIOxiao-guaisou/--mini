# 🚀 快速开始

## 1️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

## 2️⃣ 配置企业微信
编辑 `config.py`：
```python
WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```

## 3️⃣ 运行系统
```bash
python START.py
```

选择菜单：
- **1**: 离线分析（快速，<1秒）
- **2**: 在线爬取（完整流程）  
- **3**: 定时自动化

## 📊 输出文件
- `niche_report.json` - 蓝海报告
- `xhs_data.json` - 小红书数据
- `fish_data.json` - 闲鱼数据

详见 README.md
