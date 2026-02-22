# OpenCode + Oh My OpenCode 快速部署脚本 (Windows PowerShell)
# 作者：姜子牙 (Orchestrator)
# 日期：2026-01-19

Write-Host "================================" -ForegroundColor Cyan
Write-Host "小学英语教学设计智能代理系统" -ForegroundColor Cyan
Write-Host "OpenCode + Oh My OpenCode 部署" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Node.js
Write-Host "[1/8] 检查 Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js 已安装: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未检测到 Node.js，请先安装: https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# 检查 OpenCode
Write-Host "[2/8] 检查 OpenCode..." -ForegroundColor Yellow
if (Get-Command opencode -ErrorAction SilentlyContinue) {
    Write-Host "✓ OpenCode 已安装" -ForegroundColor Green
} else {
    Write-Host "⚠ 未检测到 OpenCode，正在安装..." -ForegroundColor Yellow
    npm install -g opencode
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ OpenCode 安装成功" -ForegroundColor Green
    } else {
        Write-Host "✗ OpenCode 安装失败" -ForegroundColor Red
        exit 1
    }
}

# 检查 Oh My OpenCode
Write-Host "[3/8] 检查 Oh My OpenCode..." -ForegroundColor Yellow
if (Get-Command oh-my-opencode -ErrorAction SilentlyContinue) {
    Write-Host "✓ Oh My OpenCode 已安装" -ForegroundColor Green
} else {
    Write-Host "⚠ 未检测到 Oh My OpenCode，正在安装..." -ForegroundColor Yellow
    npm install -g oh-my-opencode
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Oh My OpenCode 安装成功" -ForegroundColor Green
    } else {
        Write-Host "✗ Oh My OpenCode 安装失败" -ForegroundColor Red
        exit 1
    }
}

# 创建 .env 文件
Write-Host "[4/8] 配置环境变量..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ 已创建 .env 文件（请编辑并填入你的 API Key）" -ForegroundColor Green
} else {
    Write-Host "✓ .env 文件已存在" -ForegroundColor Green
}

# 加载环境变量
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "✓ 环境变量已加载" -ForegroundColor Green
}

# 检查 OpenRouter API Key
Write-Host "[5/8] 检查 API Key..." -ForegroundColor Yellow
if ($env:OPENROUTER_API_KEY -and $env:OPENROUTER_API_KEY -ne "sk-or-v1-your-key-here") {
    Write-Host "✓ OpenRouter API Key 已配置" -ForegroundColor Green
} else {
    Write-Host "⚠ OpenRouter API Key 未配置" -ForegroundColor Yellow
    Write-Host "  请编辑 .env 文件并填入你的 API Key" -ForegroundColor Yellow
    Write-Host "  获取地址: https://openrouter.ai/keys" -ForegroundColor Cyan
}

# 配置 OpenCode
Write-Host "[6/8] 配置 OpenCode..." -ForegroundColor Yellow
if (Test-Path "opencode.json") {
    Write-Host "✓ opencode.json 已存在" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 opencode.json" -ForegroundColor Red
    exit 1
}

# 配置 Oh My OpenCode
Write-Host "[7/8] 配置 Oh My OpenCode..." -ForegroundColor Yellow
if (Test-Path ".oh-my-opencode.config.json") {
    Write-Host "✓ .oh-my-opencode.config.json 已存在" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 .oh-my-opencode.config.json" -ForegroundColor Red
    exit 1
}

# 创建必要的目录
Write-Host "[8/8] 创建必要目录..." -ForegroundColor Yellow
$dirs = @("state", "draft", "materials", "assets", ".cache", "state/backups")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✓ 创建目录: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "接下来的步骤：" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 编辑 .env 文件，填入你的 API Key" -ForegroundColor White
Write-Host "   获取地址: https://openrouter.ai/keys" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 上传教学材料到 materials/ 文件夹：" -ForegroundColor White
Write-Host "   - 教材 → materials/textbooks/" -ForegroundColor Cyan
Write-Host "   - 课程标准 → materials/standards/" -ForegroundColor Cyan
Write-Host "   - 参考资料 → materials/reference/" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. 启动教学设计流程：" -ForegroundColor White
Write-Host "   .\start-lesson-design.ps1 ""Unit 1"" ""五年级"" ""译林版""" -ForegroundColor Cyan
Write-Host ""
Write-Host "或使用 OpenCode CLI：" -ForegroundColor White
Write-Host "   opencode" -ForegroundColor Cyan
Write-Host "   /workflow lesson_design" -ForegroundColor Cyan
Write-Host ""
Write-Host "查看文档：README_OPENCODE.md" -ForegroundColor Yellow
Write-Host ""
