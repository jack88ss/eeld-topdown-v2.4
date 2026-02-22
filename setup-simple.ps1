# OpenCode 简化版快速部署脚本（不依赖 Oh My OpenCode）
# 作者：姜子牙 (Orchestrator)
# 日期：2026-01-19

Write-Host "================================" -ForegroundColor Cyan
Write-Host "小学英语教学设计智能代理系统" -ForegroundColor Cyan
Write-Host "OpenCode 简化版部署" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Node.js
Write-Host "[1/6] 检查 Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js 已安装: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未检测到 Node.js，请先安装: https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# 检查 OpenCode
Write-Host "[2/6] 检查 OpenCode..." -ForegroundColor Yellow
if (Get-Command opencode -ErrorAction SilentlyContinue) {
    $version = opencode --version 2>&1
    Write-Host "✓ OpenCode 已安装: $version" -ForegroundColor Green
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

# 跳过 Oh My OpenCode（因为需要 Bun）
Write-Host "[3/6] 跳过 Oh My OpenCode（使用 OpenCode 原生功能）..." -ForegroundColor Yellow
Write-Host "✓ 将使用 OpenCode 原生工作流" -ForegroundColor Green

# 创建 .env 文件
Write-Host "[4/6] 配置环境变量..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✓ 已创建 .env 文件（请编辑并填入你的 API Key）" -ForegroundColor Green
    } else {
        # 创建基本的 .env 文件
        @"
# OpenCode 环境配置
OPENROUTER_API_KEY=sk-or-v1-your-key-here
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# 模型配置
DEFAULT_MODEL=openrouter/anthropic/claude-3.5-sonnet
LONG_CONTEXT_MODEL=openrouter/google/gemini-pro-1.5
FAST_MODEL=openrouter/anthropic/claude-3-haiku
CODEX_MODEL=openrouter/openai/gpt-5.2-codex

# 成本控制
COST_BUDGET_ALERT=5.0
ENABLE_COST_TRACKING=true
"@ | Out-File -FilePath ".env" -Encoding utf8
        Write-Host "✓ 已创建 .env 文件" -ForegroundColor Green
    }
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
Write-Host "[5/6] 检查 API Key..." -ForegroundColor Yellow
if ($env:OPENROUTER_API_KEY -and $env:OPENROUTER_API_KEY -ne "sk-or-v1-your-key-here") {
    Write-Host "✓ OpenRouter API Key 已配置" -ForegroundColor Green
} else {
    Write-Host "⚠ OpenRouter API Key 未配置" -ForegroundColor Yellow
    Write-Host "  请编辑 .env 文件并填入你的 API Key" -ForegroundColor Yellow
    Write-Host "  获取地址: https://openrouter.ai/keys" -ForegroundColor Cyan
}

# 创建必要的目录
Write-Host "[6/6] 创建必要目录..." -ForegroundColor Yellow
$dirs = @("state", "draft", "materials/textbooks", "materials/standards", "materials/reference", "assets", ".cache")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ 创建目录: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 系统配置：" -ForegroundColor Yellow
Write-Host "  - 使用 OpenCode v$(opencode --version 2>&1)" -ForegroundColor White
Write-Host "  - 不使用 Oh My OpenCode（简化方案）" -ForegroundColor White
Write-Host "  - 支持多模型（Gemini、Claude、GPT-5.2-Codex）" -ForegroundColor White
Write-Host ""
Write-Host "接下来的步骤：" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 编辑 .env 文件，填入你的 API Key" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Cyan
Write-Host "   获取地址: https://openrouter.ai/keys" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 上传教学材料到 materials/ 文件夹：" -ForegroundColor White
Write-Host "   - 教材 → materials\textbooks\" -ForegroundColor Cyan
Write-Host "   - 课程标准 → materials\standards\" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. 启动教学设计流程：" -ForegroundColor White
Write-Host "   .\start-lesson-design-simple.ps1 `"Unit 1`" `"五年级`" `"译林版`"" -ForegroundColor Cyan
Write-Host ""
Write-Host "或使用 OpenCode CLI：" -ForegroundColor White
Write-Host "   opencode --config opencode.json" -ForegroundColor Cyan
Write-Host ""
