# 📖 手动操作指南
## 不使用脚本，完全手动执行教学设计任务

---

## 🎯 完整手动流程（分步详解）

---

## 第1步：进入项目目录（30秒）

```powershell
# 进入项目目录
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down

# 验证当前位置
pwd
# 应显示：C:\Users\Administrator\Desktop\myproject\eeld-top-down
```

---

## 第2步：手动加载环境变量（1分钟）

```powershell
# 方法1：使用 PowerShell 脚本加载（推荐）
Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

# 验证 API Key 是否加载
echo $env:OPENROUTER_API_KEY
# 应显示：sk-or-v1-你的密钥（前几个字符）
```

**或者方法2：手动设置（如果方法1不work）**

```powershell
# 打开 .env 文件查看你的 API Key
notepad .env

# 手动设置环境变量（替换为你的真实密钥）
$env:OPENROUTER_API_KEY = "sk-or-v1-你的真实密钥"

# 验证
echo $env:OPENROUTER_API_KEY
```

---

## 第3步：启动 OpenCode（30秒）

```powershell
# 启动 OpenCode，指定配置文件
opencode --config opencode.json
```

**你会看到**：
```
OpenCode CLI v1.1.25

Type /help for available commands
Loading configuration from opencode.json...
✓ Configuration loaded
✓ Connected to OpenRouter API
✓ Models available: 4

Ready to process.
>
```

---

## 第4步：在 OpenCode 中输入完整提示词（2分钟）

**重要**：在 OpenCode 提示符 `>` 后，复制粘贴以下完整提示词：

```
你是小学英语教学设计智能代理系统的流程总指挥（Orchestrator - 姜子牙）。

请为我设计一份完整的小学英语教案：

【任务信息】
- 教学主题：Unit 1 Goldilocks and the three bears
- 年级：五年级
- 教材版本：译林版
- 时间：2026-01-19

【工作流程】
请按照以下9个阶段依次执行：

阶段1：材料审核（Material Intake）
- 扫描并读取 materials/ 文件夹中的教材和课程标准
- 使用模型：google/gemini-pro-1.5（支持大文件）
- 生成文件：state/MATERIAL_AUDIT.md
- 记录扫描的文件列表和关键信息

阶段2：课程分析（Curriculum Analysis）
- 基于教材内容分析课程目标、重难点、学情特点
- 使用模型：anthropic/claude-3.5-sonnet
- 生成文件：state/CURRICULUM_ANALYSIS.md
- 包含：教学目标、重点难点、学情分析

阶段3：内容设计（Content Design）
- 设计核心任务和语言工具准备
- 使用模型：anthropic/claude-3.5-sonnet
- 生成文件：state/CONTENT_DESIGN.md
- 包含：核心任务描述、语言工具清单、教学流程框架

阶段4：核心大任务建议（Big Task Proposal）⭐用户确认点
- 提出本节课的核心大任务建议
- 使用模型：anthropic/claude-3.5-sonnet
- 生成文件：state/BIG_TASK_PROPOSAL.md
- 包含：大任务描述、分析理由、备选方案
- 【重要】完成后暂停，等待我确认核心大任务

阶段5：活动设计（Activity Design）
- 基于确认的核心大任务设计完整活动链
- 使用模型：anthropic/claude-3.5-sonnet
- 生成文件：state/ACTIVITY_DESIGN.md
- 包含：Pre-task/While-task/Post-task 三阶段活动

阶段6：资源协调（Resource Coordination）
- 整理教学资源清单和来源
- 使用模型：anthropic/claude-3-haiku（快速）
- 生成文件：state/RESOURCE_LIST.md 和 state/SOURCES.md
- 包含：所需资源清单、获取方式、版权信息

阶段7：评估设计（Assessment Design）
- 设计评估方案和练习题
- 使用模型：anthropic/claude-3.5-sonnet
- 生成文件：state/ASSESSMENT_DESIGN.md
- 包含：评估标准、练习题、评分细则

阶段8：质量审核（Quality Review）
- 全面审核所有设计文档
- 使用模型：anthropic/claude-3.5-sonnet
- 生成文件：state/QUALITY_REVIEW.md
- 包含：审核结果、问题列表、改进建议

阶段9：打包发布（Package Publish）
- 生成完整的教案和学习材料
- 使用模型：anthropic/claude-3-haiku（快速）
- 生成文件：
  * draft/lesson_plan.md（完整教案）
  * draft/student_preview_guide.md（学生预习清单）
  * draft/homework_sheet.md（家庭作业纸）
  * draft/PACKAGE_CHECKLIST.md（交付物清单）
  * draft/USAGE_GUIDE.md（使用说明）

【重要说明】
1. 每完成一个阶段，在 state/LOG.md 中记录日志
2. 在阶段4完成后必须暂停，展示核心大任务建议，等待我确认
3. 所有文件使用 Markdown 格式
4. 遵循"任务驱动、自上而下学习法"的教学理念
5. 核心大任务必须是单一聚焦的

现在，请从阶段1（材料审核）开始执行。
```

---

## 第5步：等待 OpenCode 执行（自动）

粘贴提示词后按回车，OpenCode 会自动开始执行。

**你会看到**：
```
> [Orchestrator] 收到任务，开始执行教学设计流程...

[阶段1/9] 材料审核
[Orchestrator] 正在扫描 materials/ 文件夹...
[Orchestrator] 使用模型: google/gemini-pro-1.5
[Orchestrator] 读取文件: materials/textbooks/...
...
[Orchestrator] ✓ 材料审核完成
[Orchestrator] 生成文件: state/MATERIAL_AUDIT.md

[阶段2/9] 课程分析
[Curriculum Analyst] 开始分析课程...
[Curriculum Analyst] 使用模型: anthropic/claude-3.5-sonnet
...
```

---

## 第6步：用户确认点（重要！）⏸️

当执行到阶段4时，OpenCode 会暂停并显示：

```
[阶段4/9] 核心大任务建议

[Activity Designer] 已完成大任务建议分析

【核心大任务建议】
本节课的核心大任务为：
"续写 Goldilocks 的故事结局，并进行小组角色扮演"

【分析理由】
- 真实性：学生需要真实使用英语创作和表达
- 完整性：包含理解、创作、表演的完整过程
- 有成果：有具体的故事续写和表演作品
- 交际目的：在表演中进行真实的语言交流
- 单一聚焦：所有活动都围绕"续写和表演"展开

【备选方案】
1. 制作 Goldilocks 故事绘本
2. 设计故事新结局海报
3. 录制故事配音视频

详细信息已保存到：state/BIG_TASK_PROPOSAL.md

请选择：
1 - 确认使用建议的大任务
2 - 修改大任务（请说明如何修改）
3 - 选择备选方案（请说明选择哪个）

请输入选择（1/2/3）：_
```

**你需要做什么**：

- **查看详细建议**（可选）：
  ```powershell
  # 在另一个 PowerShell 窗口
  notepad state\BIG_TASK_PROPOSAL.md
  ```

- **在 OpenCode 中输入你的选择**：

  ```
  1
  ```
  
  然后按回车。

**或者修改**：
```
2

我想修改为："制作 Goldilocks 故事漫画，并举办班级展览"
```

**或者选择备选**：
```
3

我选择备选方案1：制作 Goldilocks 故事绘本
```

---

## 第7步：继续执行（自动）

确认后，OpenCode 会自动继续执行剩余阶段：

```
[Activity Designer] ✓ 收到用户确认
[Activity Designer] 核心大任务：续写故事并角色扮演

[阶段5/9] 活动设计
[Activity Designer] 开始设计活动链...
[Activity Designer] 使用模型: anthropic/claude-3.5-sonnet
...

[阶段6/9] 资源协调
[Resource Coordinator] 整理资源清单...
...

[阶段7/9] 评估设计
[Assessment Expert] 设计评估方案...
...

[阶段8/9] 质量审核
[Quality Reviewer] 开始质量审核...
...

[阶段9/9] 打包发布
[Package Publisher] 生成最终文档...
[Package Publisher] ✓ lesson_plan.md
[Package Publisher] ✓ student_preview_guide.md
[Package Publisher] ✓ homework_sheet.md
...

================================
✅ 教学设计流程完成！
================================

生成的文件：
- state/MATERIAL_AUDIT.md
- state/CURRICULUM_ANALYSIS.md
- state/CONTENT_DESIGN.md
- state/BIG_TASK_PROPOSAL.md
- state/ACTIVITY_DESIGN.md
- state/RESOURCE_LIST.md
- state/ASSESSMENT_DESIGN.md
- state/QUALITY_REVIEW.md
- draft/lesson_plan.md ⭐
- draft/student_preview_guide.md
- draft/homework_sheet.md
- draft/PACKAGE_CHECKLIST.md
- draft/USAGE_GUIDE.md

总耗时：12分35秒
总成本：$0.68
```

---

## 第8步：查看结果

在新的 PowerShell 窗口（或退出 OpenCode 后）：

```powershell
# 查看主教案（最重要）
notepad draft\lesson_plan.md

# 查看预习清单
notepad draft\student_preview_guide.md

# 查看作业纸
notepad draft\homework_sheet.md

# 打开文件夹查看所有文件
explorer draft\
explorer state\
```

---

## 🔍 实时监控（可选）

在执行过程中，你可以在另一个 PowerShell 窗口实时监控：

```powershell
# 窗口1：运行 OpenCode
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down
opencode --config opencode.json

# 窗口2：实时查看日志
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down
Get-Content state\LOG.md -Wait -Tail 50

# 窗口3：查看状态（可选）
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down
Get-Content state\STATUS.yaml
```

---

## 📝 完整提示词模板（不同主题）

### 示例1：人教版PEP三年级 Colours

```
你是小学英语教学设计智能代理系统的流程总指挥（Orchestrator - 姜子牙）。

请为我设计一份完整的小学英语教案：

【任务信息】
- 教学主题：Unit 2 Colours
- 年级：三年级
- 教材版本：人教版PEP
- 时间：2026-01-19

【工作流程】
（后面的内容与上面相同）
...
```

### 示例2：外研版四年级

```
你是小学英语教学设计智能代理系统的流程总指挥（Orchestrator - 姜子牙）。

请为我设计一份完整的小学英语教案：

【任务信息】
- 教学主题：Module 3 My School
- 年级：四年级
- 教材版本：外研版
- 时间：2026-01-19

【工作流程】
（后面的内容与上面相同）
...
```

---

## 💡 手动操作的优势

1. ✅ **更好的控制**：每一步都清楚知道在做什么
2. ✅ **灵活调整**：可以随时修改提示词
3. ✅ **学习理解**：理解整个系统的工作原理
4. ✅ **避免编码问题**：不依赖脚本文件
5. ✅ **调试方便**：出问题时更容易定位

---

## ⚠️ 常见问题

### Q1: 环境变量没有加载？

```powershell
# 重新加载
Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

# 或者手动设置
$env:OPENROUTER_API_KEY = "sk-or-v1-你的密钥"
```

### Q2: OpenCode 连接失败？

```powershell
# 检查 API Key
echo $env:OPENROUTER_API_KEY

# 如果为空，重新设置
$env:OPENROUTER_API_KEY = "sk-or-v1-你的密钥"

# 重新启动 OpenCode
opencode --config opencode.json
```

### Q3: 提示词太长，粘贴不进去？

**方法1**：创建提示词文件
```powershell
# 创建文件
notepad my_prompt.txt

# 粘贴提示词，保存

# 在 OpenCode 中使用
> /file my_prompt.txt
```

**方法2**：分段输入
```powershell
# 先输入基本信息
> 你是 Orchestrator，请设计教案：主题 Unit 1 Goldilocks，五年级，译林版

# 然后继续输入详细要求
> 请按照9个阶段执行：材料审核、课程分析、内容设计...
```

### Q4: 如何退出 OpenCode？

```
> /exit
```

或按 `Ctrl+C`

---

## 📊 完整操作时间线

| 步骤 | 时间 | 操作 |
|------|------|------|
| 进入目录 | 10秒 | cd 命令 |
| 加载环境变量 | 30秒 | 复制粘贴命令 |
| 启动 OpenCode | 20秒 | opencode --config |
| 输入提示词 | 1分钟 | 复制粘贴完整提示词 |
| 自动执行1-3 | 5分钟 | 等待 |
| 用户确认 | 1分钟 | 输入1并回车 |
| 自动执行5-9 | 8分钟 | 等待 |
| 查看结果 | 1分钟 | notepad 命令 |
| **总计** | **约17分钟** | - |

---

## ✅ 手动操作检查清单

执行前：
- [ ] 已进入项目目录
- [ ] 已加载环境变量
- [ ] 已验证 API Key
- [ ] 已准备完整提示词

执行中：
- [ ] OpenCode 已启动
- [ ] 提示词已输入
- [ ] 在确认点输入选择
- [ ] 观察执行进度

完成后：
- [ ] 查看 draft/lesson_plan.md
- [ ] 验证所有文件已生成
- [ ] 检查日志无错误

---

## 🎯 现在就开始手动操作！

```powershell
# 第1步：进入目录
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down

# 第2步：加载环境变量
Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

# 第3步：启动 OpenCode
opencode --config opencode.json

# 第4步：在 OpenCode 中粘贴完整提示词
# （参考上面的"第4步"部分）
```

**祝你操作顺利！** 🎉
