# 环境检查脚本 - 验证 OpenCode 是否可用
# 用法：.\check-environment.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "OpenCode 环境检查" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# 检查 Node.js
Write-Host "[1/6] 检查 Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "  ✓ Node.js 已安装: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Node.js 未安装" -ForegroundColor Red
    Write-Host "    下载地址: https://nodejs.org/" -ForegroundColor Yellow
    $allGood = $false
}
Write-Host ""

# 检查 OpenCode（全局）
Write-Host "[2/6] 检查 OpenCode（全局安装）..." -ForegroundColor Yellow
if (Get-Command opencode -ErrorAction SilentlyContinue) {
    try {
        $opencodeVersion = opencode --version 2>&1
        Write-Host "  ✓ OpenCode 已全局安装: $opencodeVersion" -ForegroundColor Green
        Write-Host "    安装位置: $(Get-Command opencode).Source" -ForegroundColor Gray
    } catch {
        Write-Host "  ⚠ OpenCode 命令存在但可能有问题" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ OpenCode 未全局安装" -ForegroundColor Red
    Write-Host "    安装命令: npm install -g opencode" -ForegroundColor Yellow
    $allGood = $false
}
Write-Host ""

# 检查 Oh My OpenCode（全局）
Write-Host "[3/6] 检查 Oh My OpenCode（全局安装）..." -ForegroundColor Yellow
if (Get-Command oh-my-opencode -ErrorAction SilentlyContinue) {
    try {
        $omoVersion = oh-my-opencode --version 2>&1
        Write-Host "  ✓ Oh My OpenCode 已全局安装: $omoVersion" -ForegroundColor Green
        Write-Host "    安装位置: $(Get-Command oh-my-opencode).Source" -ForegroundColor Gray
    } catch {
        Write-Host "  ⚠ Oh My OpenCode 命令存在但可能有问题" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ Oh My OpenCode 未全局安装" -ForegroundColor Red
    Write-Host "    安装命令: npm install -g oh-my-opencode" -ForegroundColor Yellow
    $allGood = $false
}
Write-Host ""

# 检查项目配置文件
Write-Host "[4/6] 检查项目配置文件..." -ForegroundColor Yellow
$configFiles = @(
    "opencode.json",
    ".oh-my-opencode.config.json"
)

foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file 存在" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file 不存在" -ForegroundColor Red
        $allGood = $false
    }
}
Write-Host ""

# 检查环境变量文件
Write-Host "[5/6] 检查环境变量..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env 文件存在" -ForegroundColor Green
    
    # 检查 API Key 是否配置
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENROUTER_API_KEY=sk-or-v1-[a-zA-Z0-9]") {
        Write-Host "  ✓ OPENROUTER_API_KEY 已配置" -ForegroundColor Green
    } elseif ($envContent -match "OPENROUTER_API_KEY=sk-or-v1-your-key-here") {
        Write-Host "  ⚠ OPENROUTER_API_KEY 未配置（仍是示例值）" -ForegroundColor Yellow
        Write-Host "    请编辑 .env 文件并填入真实的 API Key" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠ OPENROUTER_API_KEY 格式可能不正确" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ .env 文件不存在" -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Write-Host "    运行: Copy-Item .env.example .env" -ForegroundColor Yellow
    }
}
Write-Host ""

# 检查 Python（可选，用于 hooks）
Write-Host "[6/6] 检查 Python（可选，用于 hooks）..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "  ✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Python 未安装（可选）" -ForegroundColor Yellow
    Write-Host "    Hooks 功能需要 Python 3.8+" -ForegroundColor Gray
}
Write-Host ""

# 总结
Write-Host "================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ 环境检查完成 - 可以使用！" -ForegroundColor Green
    Write-Host ""
    Write-Host "接下来的步骤：" -ForegroundColor Yellow
    Write-Host "1. 如果 .env 文件未配置，编辑它并填入 API Key" -ForegroundColor White
    Write-Host "2. 运行: .\start-lesson-design.ps1 `"Unit 1`" `"五年级`" `"译林版`"" -ForegroundColor White
} else {
    Write-Host "⚠️ 环境检查发现问题" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请先解决上述问题，然后重新运行此脚本" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "常见解决方案：" -ForegroundColor Yellow
    Write-Host "• 安装 OpenCode: npm install -g opencode" -ForegroundColor White
    Write-Host "• 安装 Oh My OpenCode: npm install -g oh-my-opencode" -ForegroundColor White
    Write-Host "• 重启 PowerShell（使 PATH 生效）" -ForegroundColor White
}
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 显示全局 npm 包位置
Write-Host "💡 提示：全局 npm 包安装位置" -ForegroundColor Cyan
try {
    $npmRoot = npm root -g
    Write-Host "全局包目录: $npmRoot" -ForegroundColor Gray
    
    # 列出已安装的相关全局包
    $globalPackages = npm list -g --depth=0 2>&1 | Select-String -Pattern "(opencode|oh-my-opencode)"
    if ($globalPackages) {
        Write-Host ""
        Write-Host "已安装的相关全局包：" -ForegroundColor Gray
        $globalPackages | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    }
} catch {
    Write-Host "无法获取全局包信息" -ForegroundColor Gray
}
Write-Host ""
