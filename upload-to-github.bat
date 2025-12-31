@echo off
REM Git 快速上传脚本 - 用于 Windows PowerShell

REM 使用方法:
REM 1. 保存此文件为 upload-to-github.bat
REM 2. 修改 YOUR_USERNAME 为您的 GitHub 用户名
REM 3. 运行此脚本

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  GitHub 项目上传工具
echo ========================================
echo.

REM 检查 Git 是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git 未安装或未在 PATH 中
    echo 请访问 https://git-scm.com/download/win 安装 Git
    pause
    exit /b 1
)

echo [✓] Git 已安装
echo.

REM 检查是否已初始化 Git
if not exist .git (
    echo [步骤 1] 初始化 Git 仓库...
    git init
    echo [✓] Git 仓库已初始化
    echo.
) else (
    echo [✓] Git 仓库已存在
    echo.
)

REM 配置用户信息（如果还未配置）
echo [步骤 2] 配置 Git 用户信息...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo 请输入您的 GitHub 用户名:
    set /p GITHUB_NAME=
    git config user.name "!GITHUB_NAME!"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo 请输入您的 GitHub 邮箱:
    set /p GITHUB_EMAIL=
    git config user.email "!GITHUB_EMAIL!"
)
echo [✓] 用户信息已配置
echo.

REM 添加文件
echo [步骤 3] 添加文件到暂存区...
git add .
if errorlevel 1 (
    echo [ERROR] 添加文件失败
    pause
    exit /b 1
)
echo [✓] 文件已添加
echo.

REM 创建首次提交
echo [步骤 4] 创建提交...
git status --porcelain >nul
for /f "tokens=*" %%A in ('git status --porcelain') do (
    set "changed=%%A"
)

if defined changed (
    git commit -m "Initial commit: 小红书和闲鱼企业级爬虫系统"
    if errorlevel 1 (
        echo [ERROR] 创建提交失败
        pause
        exit /b 1
    )
    echo [✓] 提交已创建
) else (
    echo [√] 无新更改需要提交
)
echo.

REM 配置远程仓库
echo [步骤 5] 配置远程仓库...
echo 请输入您的 GitHub 仓库 URL
echo 例如: https://github.com/YOUR_USERNAME/iostoupin.git
echo.
set /p REPO_URL=GitHub 仓库 URL:

git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
if errorlevel 1 (
    echo [ERROR] 添加远程仓库失败
    pause
    exit /b 1
)
echo [✓] 远程仓库已配置
echo.

REM 创建 main 分支并推送
echo [步骤 6] 推送到 GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo [ERROR] 推送失败
    echo 可能的原因:
    echo 1. 仓库 URL 错误
    echo 2. 没有推送权限
    echo 3. GitHub 仓库不存在
    echo.
    echo 请检查后重新运行此脚本
    pause
    exit /b 1
)

echo.
echo ========================================
echo  [✓] 上传成功！
echo ========================================
echo.
echo 您的项目已上传到:
echo %REPO_URL%
echo.
echo 后续更新只需运行:
echo   git add .
echo   git commit -m "描述您的更改"
echo   git push
echo.
pause
