#!/usr/bin/env pwsh
<#
.SYNOPSIS
    GitHub 项目上传脚本（PowerShell 版本）

.DESCRIPTION
    用于将 iostoupin 项目快速上传到 GitHub

.EXAMPLE
    .\upload-to-github.ps1
#>

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 GitHub 项目上传工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Git
Write-Host "正在检查 Git..." -ForegroundColor Yellow
try {
    git --version | Out-Null
    Write-Host "✓ Git 已安装" -ForegroundColor Green
} catch {
    Write-Host "✗ Git 未安装或未在 PATH 中" -ForegroundColor Red
    Write-Host "请访问 https://git-scm.com/download/win 安装 Git" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# 初始化 Git
if (-not (Test-Path ".git")) {
    Write-Host "步骤 1: 初始化 Git 仓库..." -ForegroundColor Cyan
    git init
    Write-Host "✓ Git 仓库已初始化" -ForegroundColor Green
} else {
    Write-Host "✓ Git 仓库已存在" -ForegroundColor Green
}

Write-Host ""

# 配置用户信息
Write-Host "步骤 2: 配置 Git 用户信息..." -ForegroundColor Cyan

$existingName = git config user.name 2>$null
if (-not $existingName) {
    $githubName = Read-Host "请输入您的 GitHub 用户名"
    git config user.name $githubName
}

$existingEmail = git config user.email 2>$null
if (-not $existingEmail) {
    $githubEmail = Read-Host "请输入您的 GitHub 邮箱"
    git config user.email $githubEmail
}

Write-Host "✓ 用户信息已配置" -ForegroundColor Green
Write-Host ""

# 添加文件
Write-Host "步骤 3: 添加文件到暂存区..." -ForegroundColor Cyan
git add .
Write-Host "✓ 文件已添加" -ForegroundColor Green
Write-Host ""

# 创建首次提交
Write-Host "步骤 4: 创建提交..." -ForegroundColor Cyan
$status = git status --porcelain 2>$null
if ($status) {
    git commit -m "Initial commit: 小红书和闲鱼企业级爬虫系统"
    Write-Host "✓ 提交已创建" -ForegroundColor Green
} else {
    Write-Host "√ 无新更改需要提交" -ForegroundColor Yellow
}

Write-Host ""

# 配置远程仓库
Write-Host "步骤 5: 配置远程仓库..." -ForegroundColor Cyan
Write-Host ""
Write-Host "请输入您的 GitHub 仓库 URL" -ForegroundColor Yellow
Write-Host "例如: https://github.com/YOUR_USERNAME/iostoupin.git" -ForegroundColor Gray
Write-Host ""
$repoUrl = Read-Host "GitHub 仓库 URL"

if (-not $repoUrl) {
    Write-Host "✗ 仓库 URL 不能为空" -ForegroundColor Red
    exit 1
}

git remote remove origin 2>$null
git remote add origin $repoUrl

Write-Host "✓ 远程仓库已配置" -ForegroundColor Green
Write-Host ""

# 推送到 GitHub
Write-Host "步骤 6: 推送到 GitHub..." -ForegroundColor Cyan
Write-Host "第一次推送可能需要输入 GitHub 凭证..." -ForegroundColor Yellow
Write-Host ""

git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✓ 上传成功！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "您的项目已上传到:" -ForegroundColor Cyan
    Write-Host "  $repoUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "后续更新只需运行:" -ForegroundColor Cyan
    Write-Host "  git add ." -ForegroundColor Green
    Write-Host "  git commit -m '描述您的更改'" -ForegroundColor Green
    Write-Host "  git push" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ✗ 上传失败！" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因:" -ForegroundColor Yellow
    Write-Host "  1. 仓库 URL 错误" -ForegroundColor Gray
    Write-Host "  2. 没有推送权限" -ForegroundColor Gray
    Write-Host "  3. GitHub 仓库不存在" -ForegroundColor Gray
    Write-Host "  4. 网络连接问题" -ForegroundColor Gray
    Write-Host ""
    Write-Host "请检查后重新运行此脚本" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
