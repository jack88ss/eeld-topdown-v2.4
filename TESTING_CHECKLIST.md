# OpenCode 系统测试验证清单
## 确保改造成功的完整检查

---

## 📋 测试前准备

### ✅ 环境检查

```powershell
# 1. 检查 Node.js
node --version
# 应显示：v18.x.x 或更高

# 2. 检查 OpenCode
opencode --version
# 应显示版本号

# 3. 检查 Oh My OpenCode
oh-my-opencode --version
# 应显示版本号

# 4. 检查 Python（可选，用于Hooks）
python --version
# 应显示：Python 3.8+
```

### ✅ API Key 配置

```powershell
# 查看 .env 文件
cat .env

# 应包含：
# OPENROUTER_API_KEY=sk-or-v1-实际的密钥（不是example）
```

### ✅ 文件完整性

```powershell
# 检查核心配置文件
Test-Path opencode.json                      # 应返回 True
Test-Path .oh-my-opencode.config.json        # 应返回 True
Test-Path .env                               # 应返回 True

# 检查部署脚本
Test-Path setup.ps1                          # 应返回 True
Test-Path start-lesson-design.ps1            # 应返回 True

# 检查适配器
Test-Path .opencode/adapters/agent_executor.py          # 应返回 True
Test-Path .opencode/workflows/lesson_design.yaml        # 应返回 True
```

---

## 🧪 Level 1: 基础功能测试（5分钟）

### 测试1.1：OpenCode CLI 启动

```powershell
opencode
```

**预期结果：**
- ✅ 进入 OpenCode 交互式界面
- ✅ 显示欢迎信息
- ✅ 可以输入命令

**验证命令：**
```
/help        # 显示帮助信息
/models      # 列出可用模型
/status      # 显示系统状态
/exit        # 退出
```

### 测试1.2：配置文件加载

```powershell
opencode --config opencode.json --validate
```

**预期结果：**
- ✅ 配置文件验证通过
- ✅ 无错误信息
- ✅ 显示加载的提供商和模型

### 测试1.3：API 连接测试

```powershell
opencode --provider openrouter --test-connection
```

**预期结果：**
- ✅ OpenRouter API 连接成功
- ✅ API Key 验证通过
- ✅ 显示可用的模型列表

---

## 🧪 Level 2: 代理系统测试（10分钟）

### 测试2.1：单个代理执行

```powershell
# 测试 Orchestrator 代理
python .opencode/adapters/agent_executor.py orchestrator material_intake \
  --input test_input.json
```

**预期结果：**
- ✅ 代理配置加载成功
- ✅ 选择了正确的模型（long_context）
- ✅ 日志记录到 `state/LOG.md`

### 测试2.2：模型选择验证

检查 `state/LOG.md` 最后几行：

```markdown
| 2026-01-19... | orchestrator | start | material_intake | {"model": "openrouter/google/gemini-pro-1.5"} |
```

**预期：**
- ✅ 材料审核任务选择了 `gemini-pro-1.5` (长文本模型)
- ✅ 课程分析任务选择了 `claude-3.5-sonnet` (推理模型)

---

## 🧪 Level 3: 工作流测试（20分钟）

### 测试3.1：完整工作流（小测试）

准备测试数据：

```powershell
# 1. 创建简单的测试教材
New-Item -Path "materials/textbooks/test.txt" -ItemType File -Value "Test Unit 1: Hello World"

# 2. 启动工作流
.\start-lesson-design.ps1 "Test Unit" "五年级" "测试版"
```

**监控进度：**
```powershell
# 在另一个窗口
Get-Content state/LOG.md -Wait -Tail 20
```

**预期流程：**
1. ✅ Orchestrator 启动
2. ✅ 材料审核（使用 Gemini Pro 1.5）
3. ✅ 课程分析（使用 Claude 3.5 Sonnet）
4. ✅ 内容设计（使用 Claude 3.5 Sonnet）
5. ⏸️ **暂停等待用户确认核心大任务**
6. ➡️ 输入 `1` 确认
7. ✅ 活动设计（使用 Claude 3.5 Sonnet）
8. ✅ 资源协调（使用 Claude 3 Haiku）
9. ✅ 评估设计（使用 Claude 3.5 Sonnet）
10. ✅ 质量审核（使用 Claude 3.5 Sonnet）
11. ✅ 打包发布（使用 Claude 3 Haiku）

**验证输出：**
```powershell
# 检查生成的文件
ls draft/
# 应包含：
# - lesson_plan.md
# - student_preview_guide.md
# - homework_sheet.md
# - PACKAGE_CHECKLIST.md
# - USAGE_GUIDE.md
```

### 测试3.2：用户确认点测试

在 `big_task_proposal` 阶段：

**场景A：确认建议**
```
你的选择：1
```
**预期：** 系统记录确认并继续

**场景B：修改建议**
```
你的选择：2
请描述你希望的核心大任务：制作班级故事书
```
**预期：** 系统记录修改并使用新的大任务

**场景C：选择备选方案**
```
你的选择：3
```
**预期：** 显示备选方案列表供选择

---

## 🧪 Level 4: 多模型测试（15分钟）

### 测试4.1：大文件处理（Gemini Pro 1.5）

```powershell
# 1. 上传一个大型PDF（如24MB的教材）
Copy-Item "path/to/large.pdf" "materials/textbooks/"

# 2. 启动流程
.\start-lesson-design.ps1 "Unit 1" "五年级" "译林版"

# 3. 观察日志
Get-Content state/LOG.md -Tail 50
```

**查找关键日志：**
```markdown
【模型选择】
- 原始模型：anthropic/claude-3.5-sonnet
- 检测到大文件，切换模型
- 最终模型：google/gemini-pro-1.5
- 原因：支持100万token上下文
```

**预期：**
- ✅ 系统自动检测大文件
- ✅ 自动切换到 Gemini Pro 1.5
- ✅ 成功读取PDF内容
- ✅ 生成材料审核报告

### 测试4.2：成本优化验证

查看 `state/cost.log`：

```powershell
cat state/cost.log
```

**预期成本分布：**
```
material_intake:      $0.19  (Gemini Pro 1.5)
curriculum_analysis:  $0.08  (Claude 3.5 Sonnet)
content_design:       $0.08  (Claude 3.5 Sonnet)
activity_design:      $0.10  (Claude 3.5 Sonnet)
resource_coordination:$0.004 (Claude 3 Haiku) ← 便宜！
...
总计: ~$0.67
```

**验证：**
- ✅ 简单任务使用 Haiku（便宜）
- ✅ 复杂任务使用 Sonnet（高质量）
- ✅ 长文本任务使用 Gemini（大上下文）
- ✅ 总成本在 $0.60-$0.80 之间

### 测试4.3：GPT-5.2-Codex 测试（可选）

如果配置了 GPT-5.2-Codex：

```powershell
opencode --model codex --task "生成一个自动评分的Python脚本"
```

**预期：**
- ✅ 使用 `openrouter/openai/gpt-5.2-codex`
- ✅ 生成高质量代码
- ✅ 包含完整的注释和文档

---

## 🧪 Level 5: 错误处理测试（10分钟）

### 测试5.1：API Key 错误

```powershell
# 1. 临时设置错误的 API Key
$env:OPENROUTER_API_KEY = "sk-invalid-key"

# 2. 启动流程
.\start-lesson-design.ps1 "Test" "五年级" "测试版"
```

**预期：**
- ✅ 系统检测到 API 错误
- ✅ 显示清晰的错误消息
- ✅ 提示用户检查 API Key
- ✅ 不会崩溃

### 测试5.2：文件不存在错误

```powershell
# 启动流程但不上传教材
.\start-lesson-design.ps1 "Unit X" "五年级" "不存在版"
```

**预期：**
- ✅ 系统检测到材料缺失
- ✅ 提示用户上传教材
- ✅ 提供清晰的错误消息

### 测试5.3：上下文过长错误

（如果配置正确，这个错误应该被自动处理）

**预期：**
- ✅ 系统检测到 `context_length_exceeded`
- ✅ 自动应用智能分块（smart_chunking）
- ✅ 或自动切换到长上下文模型
- ✅ 继续执行任务

---

## 🧪 Level 6: 性能测试（5分钟）

### 测试6.1：执行时间

记录各阶段时间：

```powershell
# 在启动前
$startTime = Get-Date

# 启动流程
.\start-lesson-design.ps1 "Unit 1" "五年级" "译林版"

# 完成后
$endTime = Get-Date
$duration = $endTime - $startTime
Write-Host "总耗时: $($duration.TotalMinutes) 分钟"
```

**预期时间：**
- ✅ 材料审核：1-2分钟
- ✅ 课程分析：1-2分钟
- ✅ 内容设计：2-3分钟
- ✅ 活动设计：2-3分钟
- ✅ 其他阶段：各1-2分钟
- ✅ **总计：10-15分钟**

### 测试6.2：Token 使用统计

查看 `state/LOG.md` 中的 Token 统计：

```markdown
【Token使用】
- 输入tokens：220,000
- 输出tokens：31,000
- 总计：251,000
```

**验证：**
- ✅ 总 Token 数合理（20-30万）
- ✅ 输入/输出比例合理（约7:1）
- ✅ 没有异常高的 Token 使用

---

## 📊 测试结果记录表

| 测试项 | 状态 | 说明 |
|--------|------|------|
| **Level 1: 基础功能** |||
| OpenCode CLI 启动 | ⬜️ | |
| 配置文件加载 | ⬜️ | |
| API 连接测试 | ⬜️ | |
| **Level 2: 代理系统** |||
| 单个代理执行 | ⬜️ | |
| 模型选择验证 | ⬜️ | |
| **Level 3: 工作流** |||
| 完整工作流 | ⬜️ | |
| 用户确认点 | ⬜️ | |
| **Level 4: 多模型** |||
| 大文件处理 | ⬜️ | |
| 成本优化 | ⬜️ | |
| GPT-5.2-Codex（可选） | ⬜️ | |
| **Level 5: 错误处理** |||
| API Key 错误 | ⬜️ | |
| 文件不存在错误 | ⬜️ | |
| 上下文过长错误 | ⬜️ | |
| **Level 6: 性能** |||
| 执行时间 | ⬜️ | 实际：___ 分钟 |
| Token 使用 | ⬜️ | 实际：___ tokens |
| 成本 | ⬜️ | 实际：$___ |

---

## ✅ 测试通过标准

### 必需通过（Level 1-3）

- ✅ OpenCode 能正常启动
- ✅ API 连接成功
- ✅ 完整工作流能执行完成
- ✅ 生成了完整的教案文档
- ✅ 用户确认点正常工作

### 建议通过（Level 4-6）

- ✅ 大文件能正常处理
- ✅ 成本在预期范围内（$0.60-$0.80）
- ✅ 错误处理正常
- ✅ 执行时间合理（10-20分钟）

---

## 🐛 常见问题排查

### 问题1：OpenCode 无法启动

**排查步骤：**
```powershell
# 1. 检查安装
npm list -g opencode

# 2. 重新安装
npm uninstall -g opencode
npm install -g opencode

# 3. 清理缓存
npm cache clean --force
```

### 问题2：API 连接失败

**排查步骤：**
```powershell
# 1. 检查网络
Test-Connection openrouter.ai

# 2. 检查 API Key
echo $env:OPENROUTER_API_KEY

# 3. 手动测试 API
curl -H "Authorization: Bearer $env:OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models
```

### 问题3：模型选择错误

**排查步骤：**
```powershell
# 1. 检查配置文件
cat opencode.json | Select-String "models"

# 2. 验证模型可用性
opencode --list-models --provider openrouter

# 3. 查看日志中的模型选择
cat state/LOG.md | Select-String "模型选择"
```

---

## 📝 测试报告模板

完成测试后，填写以下报告：

```markdown
# OpenCode 系统测试报告

**测试日期**：2026-01-19
**测试人员**：[你的名字]
**系统版本**：v2.4.0-OpenCode

## 测试环境
- 操作系统：Windows 11
- Node.js 版本：v18.x.x
- OpenCode 版本：x.x.x
- Oh My OpenCode 版本：x.x.x

## 测试结果总结
- 总测试项：[数量]
- 通过：[数量]
- 失败：[数量]
- 跳过：[数量]

## 详细结果
[填写测试结果记录表]

## 发现的问题
1. [问题描述]
   - 严重程度：High/Medium/Low
   - 解决方案：[描述]

## 性能指标
- 平均执行时间：[X] 分钟
- 平均Token使用：[X] tokens
- 平均成本：$[X]

## 建议和改进
1. [建议1]
2. [建议2]

## 结论
✅ 系统可以投入使用
⚠️ 有小问题但可以使用
❌ 需要修复后再使用
```

---

**祝测试顺利！** 🎉

如有问题，请查看 `README_OPENCODE.md` 或联系技术支持。
