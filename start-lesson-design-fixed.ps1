# Startup Script for Lesson Design (Fixed Encoding)
# Usage: .\start-lesson-design-fixed.ps1 "Unit 1" "Grade 5" "Yilin"

param(
    [Parameter(Mandatory=$true)]
    [string]$Topic,
    
    [Parameter(Mandatory=$true)]
    [string]$Grade,
    
    [Parameter(Mandatory=$true)]
    [string]$Textbook
)

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting Lesson Design Workflow" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Topic: $Topic" -ForegroundColor Yellow
Write-Host "Grade: $Grade" -ForegroundColor Yellow
Write-Host "Textbook: $Textbook" -ForegroundColor Yellow
Write-Host ""

# Load environment variables
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "Environment variables loaded" -ForegroundColor Green
}

# Check API Key
if (!$env:OPENROUTER_API_KEY -or $env:OPENROUTER_API_KEY -eq "sk-or-v1-your-key-here") {
    Write-Host "ERROR: OpenRouter API Key not configured" -ForegroundColor Red
    Write-Host "  Please edit .env file and add your API Key" -ForegroundColor Yellow
    Write-Host "  Get it from: https://openrouter.ai/keys" -ForegroundColor Cyan
    exit 1
}

Write-Host "API Key configured" -ForegroundColor Green
Write-Host ""

# Create context file
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$contextFile = "context.json"
@{
    topic = $Topic
    grade = $Grade
    textbook = $Textbook
    timestamp = $timestamp
} | ConvertTo-Json | Out-File -FilePath $contextFile -Encoding utf8

# Create prompt file
$promptFile = "lesson_design_prompt.txt"
$prompt = @"
You are the Orchestrator (Jiang Ziya) of the elementary English lesson design system.

Task Information:
- Topic: $Topic
- Grade: $Grade
- Textbook: $Textbook
- Timestamp: $timestamp

Please execute the complete lesson design workflow:

1. Material Intake - Review uploaded materials (use google/gemini-pro-1.5 for large PDFs)
2. Curriculum Analysis - Analyze objectives and students (use anthropic/claude-3.5-sonnet)
3. Content Design - Design core tasks (use anthropic/claude-3.5-sonnet)
4. Big Task Proposal - Propose core task (PAUSE for user confirmation)
5. Activity Design - Design activity chain (use anthropic/claude-3.5-sonnet)
6. Resource Coordination - Organize resources (use anthropic/claude-3-haiku)
7. Assessment Design - Design assessments (use anthropic/claude-3.5-sonnet)
8. Quality Review - Review quality (use anthropic/claude-3.5-sonnet)
9. Package Publish - Generate final documents (use anthropic/claude-3-haiku)

Generate files in:
- state/ - Process documents
- draft/ - Final deliverables

Start with material intake task.
"@

$prompt | Out-File -FilePath $promptFile -Encoding utf8

Write-Host "Prompt file created: $promptFile" -ForegroundColor Green
Write-Host ""

# Launch OpenCode
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Launching OpenCode Workflow" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting OpenCode..." -ForegroundColor Yellow
Write-Host "In OpenCode, the workflow will execute automatically." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to start OpenCode..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

opencode --config opencode.json

# Cleanup
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Workflow Complete or Interrupted" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "View results:" -ForegroundColor Yellow
Write-Host "  - Logs: state\LOG.md" -ForegroundColor White
Write-Host "  - Lesson Plan: draft\lesson_plan.md" -ForegroundColor White
Write-Host "  - Preview Guide: draft\student_preview_guide.md" -ForegroundColor White
Write-Host "  - Homework: draft\homework_sheet.md" -ForegroundColor White
Write-Host ""
