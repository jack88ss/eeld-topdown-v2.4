# 启动教学设计流程（简化版 - 仅使用 OpenCode）
# 用法：.\start-lesson-design-simple.ps1 "Unit 1 Goldilocks" "五年级" "译林版"

param(
    [Parameter(Mandatory=$true)]
    [string]$Topic,
    
    [Parameter(Mandatory=$true)]
    [string]$Grade,
    
    [Parameter(Mandatory=$true)]
    [string]$Textbook
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "启动教学设计流程（OpenCode版）" -ForegroundColor Cyan
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
    Write-Host "✓ 环境变量已加载" -ForegroundColor Green
}

# 检查 API Key
if (!$env:OPENROUTER_API_KEY -or $env:OPENROUTER_API_KEY -eq "sk-or-v1-your-key-here") {
    Write-Host "✗ 错误: OpenRouter API Key 未配置" -ForegroundColor Red
    Write-Host "  请编辑 .env 文件并填入你的 API Key" -ForegroundColor Yellow
    Write-Host "  获取地址: https://openrouter.ai/keys" -ForegroundColor Cyan
    exit 1
}

Write-Host "✓ API Key 已配置" -ForegroundColor Green
Write-Host ""

# 创建上下文文件
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$contextFile = "context.json"
@{
    topic = $Topic
    grade = $Grade
    textbook = $Textbook
    timestamp = $timestamp
} | ConvertTo-Json | Out-File -FilePath $contextFile -Encoding utf8

Write-Host "正在启动 OpenCode..." -ForegroundColor Yellow
Write-Host ""

# 创建提示词文件
$promptFile = "lesson_design_prompt.txt"
$prompt = @"
你是小学英语教学设计智能代理系统的流程总指挥（Orchestrator - 姜子牙）。

任务信息：
- 教学主题：$Topic
- 年级：$Grade
- 教材版本：$Textbook
- 时间戳：$timestamp

请按照以下工作流程完成教学设计：

1. 材料审核（Material Intake）
   - 读取 materials/ 文件夹中的教材和课程标准
   - 生成 state/MATERIAL_AUDIT.md
   - 使用模型：google/gemini-pro-1.5（支持长文本）

2. 课程分析（Curriculum Analysis）
   - 分析课程目标、重难点、学情
   - 生成 state/CURRICULUM_ANALYSIS.md
   - 使用模型：anthropic/claude-3.5-sonnet

3. 内容设计（Content Design）
   - 设计核心任务和教学内容
   - 生成 state/CONTENT_DESIGN.md
   - 使用模型：anthropic/claude-3.5-sonnet

4. 核心大任务建议（Big Task Proposal）
   - 提出核心大任务建议
   - 生成 state/BIG_TASK_PROPOSAL.md
   - 【暂停】等待用户确认
   - 使用模型：anthropic/claude-3.5-sonnet

5. 活动设计（Activity Design）
   - 基于确认的大任务设计活动链
   - 生成 state/ACTIVITY_DESIGN.md
   - 使用模型：anthropic/claude-3.5-sonnet

6. 资源协调（Resource Coordination）
   - 整理资源清单
   - 生成 state/RESOURCE_LIST.md
   - 使用模型：anthropic/claude-3-haiku（快速）

7. 评估设计（Assessment Design）
   - 设计评估方案
   - 生成 state/ASSESSMENT_DESIGN.md
   - 使用模型：anthropic/claude-3.5-sonnet

8. 质量审核（Quality Review）
   - 全面审核
   - 生成 state/QUALITY_REVIEW.md
   - 使用模型：anthropic/claude-3.5-sonnet

9. 打包发布（Package Publish）
   - 生成完整教案
   - 生成 draft/lesson_plan.md, draft/student_preview_guide.md, draft/homework_sheet.md
   - 使用模型：anthropic/claude-3-haiku（快速）

请开始执行材料审核任务。
"@

$prompt | Out-File -FilePath $promptFile -Encoding utf8

Write-Host "✓ 提示词已生成: $promptFile" -ForegroundColor Green
Write-Host ""

# 使用 OpenCode 执行
Write-Host "================================" -ForegroundColor Cyan
Write-Host "开始执行教学设计工作流" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 方式1：交互式（推荐）
Write-Host "启动 OpenCode 交互模式..." -ForegroundColor Yellow
Write-Host "在 OpenCode 中输入以下命令：" -ForegroundColor Cyan
Write-Host ""
Write-Host "  /file $promptFile" -ForegroundColor White
Write-Host "  /context $contextFile" -ForegroundColor White
Write-Host ""
Write-Host "或者直接粘贴提示词内容并开始对话。" -ForegroundColor Gray
Write-Host ""
Write-Host "按任意键启动 OpenCode..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

opencode --config opencode.json

# 清理临时文件
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "工作流已完成或中断" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "查看结果：" -ForegroundColor Yellow
Write-Host "  - 实时日志: state\LOG.md" -ForegroundColor White
Write-Host "  - 最终教案: draft\lesson_plan.md" -ForegroundColor White
Write-Host "  - 预习清单: draft\student_preview_guide.md" -ForegroundColor White
Write-Host "  - 作业纸: draft\homework_sheet.md" -ForegroundColor White
Write-Host ""
