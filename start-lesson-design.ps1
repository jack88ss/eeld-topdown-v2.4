# 启动教学设计流程脚本 (Windows PowerShell)
# 用法：.\start-lesson-design.ps1 "Unit 1 Goldilocks" "五年级" "译林版"

param(
    [Parameter(Mandatory=$true)]
    [string]$Topic,
    
    [Parameter(Mandatory=$true)]
    [string]$Grade,
    
    [Parameter(Mandatory=$true)]
    [string]$Textbook
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "启动教学设计流程" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "主题: $Topic" -ForegroundColor Yellow
Write-Host "年级: $Grade" -ForegroundColor Yellow
Write-Host "教材: $Textbook" -ForegroundColor Yellow
Write-Host ""

# 加载环境变量
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
}

# 检查 API Key
if (!$env:OPENROUTER_API_KEY -or $env:OPENROUTER_API_KEY -eq "sk-or-v1-your-key-here") {
    Write-Host "✗ 错误: OpenRouter API Key 未配置" -ForegroundColor Red
    Write-Host "  请编辑 .env 文件并填入你的 API Key" -ForegroundColor Yellow
    Write-Host "  获取地址: https://openrouter.ai/keys" -ForegroundColor Cyan
    exit 1
}

# 创建任务上下文
$context = @{
    topic = $Topic
    grade = $Grade
    textbook = $Textbook
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
} | ConvertTo-Json

# 使用 Oh My OpenCode 启动工作流
Write-Host "正在启动工作流..." -ForegroundColor Yellow
Write-Host ""

# 方案1：使用 OpenCode CLI
Write-Host "使用 OpenCode CLI 模式..." -ForegroundColor Cyan
opencode --config opencode.json --context $context

# 方案2：使用 Oh My OpenCode
# Write-Host "使用 Oh My OpenCode 模式..." -ForegroundColor Cyan
# oh-my-opencode workflow run lesson_design --context $context

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "工作流已启动" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "实时日志: state/LOG.md" -ForegroundColor Yellow
Write-Host "状态跟踪: state/STATUS.yaml" -ForegroundColor Yellow
Write-Host "成本跟踪: state/cost.log" -ForegroundColor Yellow
Write-Host ""
