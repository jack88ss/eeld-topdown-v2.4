# Bun 安装脚本（Windows PowerShell）
# Bun 是 Oh My OpenCode 的运行时依赖

Write-Host "================================" -ForegroundColor Cyan
Write-Host "安装 Bun for Oh My OpenCode" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Bun 是什么？" -ForegroundColor Yellow
Write-Host "Bun 是一个快速的 JavaScript 运行时，类似于 Node.js" -ForegroundColor Gray
Write-Host "Oh My OpenCode 使用 Bun 来提供增强功能" -ForegroundColor Gray
Write-Host ""

# 检查是否已安装
Write-Host "[1/4] 检查 Bun 是否已安装..." -ForegroundColor Yellow
if (Get-Command bun -ErrorAction SilentlyContinue) {
    $bunVersion = bun --version
    Write-Host "✓ Bun 已安装: $bunVersion" -ForegroundColor Green
    Write-Host ""
    Write-Host "是否要重新安装/更新？(y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "跳过安装" -ForegroundColor Gray
        exit 0
    }
}

# 方法1：使用官方安装脚本（推荐）
Write-Host "[2/4] 方法1：使用官方安装脚本..." -ForegroundColor Yellow
Write-Host "正在下载并执行 Bun 安装脚本..." -ForegroundColor Gray
Write-Host ""

try {
    # 下载并执行官方安装脚本
    irm bun.sh/install.ps1 | iex
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Bun 安装成功！" -ForegroundColor Green
    } else {
        throw "安装脚本执行失败"
    }
} catch {
    Write-Host "✗ 方法1失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "尝试方法2..." -ForegroundColor Yellow
    Write-Host ""
    
    # 方法2：使用 npm 安装
    Write-Host "[3/4] 方法2：使用 npm 安装..." -ForegroundColor Yellow
    try {
        npm install -g bun
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Bun 通过 npm 安装成功！" -ForegroundColor Green
        } else {
            throw "npm 安装失败"
        }
    } catch {
        Write-Host "✗ 方法2也失败了" -ForegroundColor Red
        Write-Host ""
        Write-Host "请手动安装：" -ForegroundColor Yellow
        Write-Host "1. 访问: https://bun.sh/docs/installation" -ForegroundColor Cyan
        Write-Host "2. 下载 Windows 安装包" -ForegroundColor Cyan
        Write-Host "3. 运行安装程序" -ForegroundColor Cyan
        exit 1
    }
}

Write-Host ""
Write-Host "[4/4] 验证安装..." -ForegroundColor Yellow

# 刷新 PATH（可能需要）
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 验证 Bun
Write-Host "检查 Bun..." -ForegroundColor Gray
if (Get-Command bun -ErrorAction SilentlyContinue) {
    $bunVersion = bun --version
    Write-Host "✓ Bun 版本: $bunVersion" -ForegroundColor Green
    Write-Host "✓ Bun 安装位置: $((Get-Command bun).Source)" -ForegroundColor Green
} else {
    Write-Host "⚠ Bun 命令未找到" -ForegroundColor Yellow
    Write-Host "  可能需要重启 PowerShell 以刷新 PATH" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请执行：" -ForegroundColor Yellow
    Write-Host "  1. 关闭此 PowerShell 窗口" -ForegroundColor Cyan
    Write-Host "  2. 重新打开 PowerShell" -ForegroundColor Cyan
    Write-Host "  3. 运行: bun --version" -ForegroundColor Cyan
    exit 0
}

Write-Host ""

# 验证 Oh My OpenCode
Write-Host "检查 Oh My OpenCode..." -ForegroundColor Gray
if (Get-Command oh-my-opencode -ErrorAction SilentlyContinue) {
    try {
        $omoVersion = oh-my-opencode --version 2>&1
        Write-Host "✓ Oh My OpenCode 版本: $omoVersion" -ForegroundColor Green
        Write-Host "✓ Oh My OpenCode 已就绪！" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Oh My OpenCode 命令存在但可能有问题" -ForegroundColor Yellow
        Write-Host "  错误信息: $_" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠ Oh My OpenCode 未安装" -ForegroundColor Yellow
    Write-Host "  安装命令: npm install -g oh-my-opencode" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "接下来的步骤：" -ForegroundColor Yellow
Write-Host "1. 验证安装:" -ForegroundColor White
Write-Host "   bun --version" -ForegroundColor Cyan
Write-Host "   oh-my-opencode --version" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 如果命令未找到，请重启 PowerShell" -ForegroundColor White
Write-Host ""
Write-Host "3. 运行完整版部署:" -ForegroundColor White
Write-Host "   .\setup.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. 启动教学设计:" -ForegroundColor White
Write-Host "   .\start-lesson-design.ps1 `"Unit 1`" `"五年级`" `"译林版`"" -ForegroundColor Cyan
Write-Host ""
