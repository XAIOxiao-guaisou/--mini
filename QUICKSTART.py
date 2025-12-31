#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 爬虫快速启动脚本
完整的持久化登录工作流程指导
"""

import os
import sys
import subprocess
from pathlib import Path

def print_colored(text, color='cyan'):
    """彩色打印"""
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'cyan': '\033[96m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    
    c = colors.get(color, colors['cyan'])
    end = colors['end']
    
    if 'bold' in color:
        print(f"{colors['bold']}{colors.get(color.replace('_bold', ''), colors['cyan'])}{text}{end}")
    else:
        print(f"{c}{text}{end}")

def main():
    os.chdir(os.path.dirname(__file__) or '.')
    
    print_colored("\n" + "="*80, "cyan")
    print_colored("🚀 小红书 + 闲鱼 爬虫 - 持久化登录快速启动", "cyan")
    print_colored("="*80 + "\n", "cyan")
    
    print_colored("📋 使用步骤：", "bold")
    print("""
1️⃣  【首次使用】 运行登录脚本
    python login_helper.py
    
    → 浏览器会打开，请手动登录小红书和闲鱼
    → 完成登录后，浏览器会自动关闭
    → ✅ 登录信息会保存到 browser_profile/

2️⃣  【后续使用】 运行爬虫
    python main.py
    
    → 选择菜单选项：
       [1] 验证系统完整性
       [2] 检查浏览器配置
       [3] 获取小红书趋势数据
       [4] 获取闲鱼二手商品数据
       [5] 系统诊断和修复
       [0] 退出

3️⃣  【如果遇到问题】
    python main.py
    → 选择 [5] 系统诊断

💡 重要提示：
   • 第一次运行 login_helper.py 时，请选择"可见"模式（不要隐藏浏览器）
   • 系统会自动保存登录状态，下次不需要重新登录
   • 如果 Cookies 过期，再次运行 login_helper.py 重新登录即可
""")
    
    # 检查系统状态
    profile_path = Path("./browser_profile")
    has_data = profile_path.exists() and any(profile_path.iterdir())
    
    print_colored("\n📊 当前系统状态：\n", "bold")
    
    if has_data:
        try:
            size_mb = sum(f.stat().st_size for f in profile_path.rglob('*') if f.is_file()) / 1024 / 1024
            print_colored(f"✅ 已找到保存的登录数据（{size_mb:.1f} MB）", "green")
            print_colored("   → 可以直接运行 python main.py 开始爬虫\n", "green")
        except:
            print_colored("✅ browser_profile 目录已存在", "green")
            print_colored("   → 可以直接运行 python main.py 开始爬虫\n", "green")
    else:
        print_colored("⚠️  尚未进行首次登录", "yellow")
        print_colored("   → 请先运行 python login_helper.py 进行登录\n", "yellow")
    
    # 给用户菜单
    print_colored("🎯 选择下一步操作：\n", "bold")
    print("""
    [1] 运行登录脚本（首次登录或重新登录）
        python login_helper.py
    
    [2] 运行爬虫系统（需要已登录）
        python main.py
    
    [3] 查看修复文档
        更多信息请查看：PERSISTENT_LOGIN_FIX.md
    
    [0] 退出
""")
    
    choice = input("请选择 [0-3]：").strip()
    
    print()
    
    if choice == '1':
        print_colored("🔐 启动登录脚本...\n", "cyan")
        os.system("python login_helper.py")
    elif choice == '2':
        print_colored("🚀 启动爬虫系统...\n", "cyan")
        os.system("python main.py")
    elif choice == '3':
        print_colored("📖 修复文档：PERSISTENT_LOGIN_FIX.md\n", "cyan")
        if os.name == 'nt':  # Windows
            os.system("notepad PERSISTENT_LOGIN_FIX.md")
        else:
            os.system("cat PERSISTENT_LOGIN_FIX.md | less")
    elif choice == '0':
        print_colored("👋 再见！\n", "cyan")
        sys.exit(0)
    else:
        print_colored("❌ 无效选择\n", "red")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  用户中断\n", "yellow")
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n❌ 错误：{e}\n", "red")
        sys.exit(1)
