# ✅ 正确的启动流程

## 重要说明

**Oh My OpenCode 是 OpenCode 的插件，不是独立命令！**

正确用法：
1. ✅ 安装 oh-my-opencode 插件
2. ✅ 在 opencode.json 中启用插件
3. ✅ 直接使用 `opencode` 命令
4. ✅ 插件自动增强功能

---

## 🚀 快速启动（2步）

### 第1步：进入项目目录 + 加载环境变量

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
Get-Content .env | ForEach-Object { if ($_ -match "^\s*([^#][^=]+)=(.*)$") { $name = $matches[1].Trim(); $value = $matches[2].Trim(); [Environment]::SetEnvironmentVariable($name, $value, "Process") } }
```

### 第2步：启动 OpenCode（插件自动加载）

```powershell
opencode --config opencode.json
```

---

## 📝 在 OpenCode 中使用 Oh My OpenCode 功能

根据 [Oh My OpenCode 文档](https://github.com/code-yeongyu/oh-my-opencode)，有几种使用方式：

### 方式1：Ultrawork 模式（最强大）🔥

在 OpenCode 提示符输入：

```
ulw Design a complete elementary English lesson plan:
- Topic: Unit 1 Goldilocks and the three bears
- Grade: 5th grade
- Textbook: Yilin Edition

Follow the 9-stage workflow (material intake → curriculum analysis → content design → big task proposal → activity design → resource coordination → assessment design → quality review → package publish).

Pause at stage 4 for user confirmation.
```

**`ulw` = ultrawork 的缩写**。Sisyphus agent 会自动：
- ✅ 分析项目结构
- ✅ 收集上下文
- ✅ 按照 TODO 列表工作
- ✅ 直到任务 100% 完成

### 方式2：Ultrathink 模式（深度思考）

```
ultrathink Analyze the best approach for designing a task-driven lesson for elementary students
```

### 方式3：直接描述任务（普通模式）

```
Design a lesson plan for Unit 1 Goldilocks, Grade 5, Yilin Edition.
```

---

## 🎯 一行启动命令（最简单）

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'; Get-Content .env | ForEach-Object { if ($_ -match "^\s*([^#][^=]+)=(.*)$") { $name = $matches[1].Trim(); $value = $matches[2].Trim(); [Environment]::SetEnvironmentVariable($name, $value, "Process") } }; opencode --config opencode.json
```

复制粘贴这一行，回车，然后输入你的任务（带 `ulw` 前缀）。

---

## 🛠️ 或使用启动脚本

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
.\.opencode\start-with-plugin.ps1
```

---

## ✨ Oh My OpenCode 的主要功能

### 1. Sisyphus Agent（主力）
- 使用 `ulw` 关键词激活
- 自动分析项目、收集上下文
- 执行完整工作流直到任务完成
- 自动管理 TODO 列表

### 2. Background Agents（后台代理）
- 可以并行运行多个 agents
- 像真实开发团队一样工作

### 3. Built-in MCPs
- websearch（Exa）
- context7（文档搜索）
- grep_app（GitHub 搜索）

### 4. LSP & AST Tools
- 重构、重命名、诊断
- AST-aware 代码搜索

### 5. Productivity Features
- Todo Enforcer：强制完成 TODO
- Comment Checker：清理无用注释
- Think Mode：深度思考模式

---

## 📋 完整示例

### 打开 PowerShell

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
Get-Content .env | ForEach-Object { if ($_ -match "^\s*([^#][^=]+)=(.*)$") { $name = $matches[1].Trim(); $value = $matches[2].Trim(); [Environment]::SetEnvironmentVariable($name, $value, "Process") } }
opencode --config opencode.json
```

### 在 OpenCode 中输入

```
ulw Design a complete lesson plan:
- Topic: Unit 1 Goldilocks and the three bears
- Grade: 五年级
- Textbook: 译林版

Execute the 9-stage workflow:
1. Material intake (scan materials/)
2. Curriculum analysis
3. Content design
4. Big task proposal (pause for confirmation)
5. Activity design
6. Resource coordination
7. Assessment design
8. Quality review
9. Package publish

Generate:
- draft/lesson_plan.md
- draft/student_preview_guide.md
- draft/homework_sheet.md

All documents in state/ and draft/ folders.
```

### Sisyphus 会自动

1. ✅ 读取 AGENTS.md 理解项目架构
2. ✅ 扫描 materials/ 文件夹
3. ✅ 按照 9 个阶段执行
4. ✅ 在阶段 4 暂停等待确认
5. ✅ 生成所有文档
6. ✅ 记录日志到 state/LOG.md
7. ✅ 完成 TODO 列表

---

## 🎯 关键区别

### ❌ 错误理解
```powershell
oh-my-opencode run --workflow lesson_design_workflow
# 这个命令不存在！
```

### ✅ 正确用法
```powershell
opencode --config opencode.json
# 然后在 OpenCode 中使用 'ulw' 关键词
```

---

## 📚 配置文件

### 1. opencode.json（主配置）
- 添加了 `"plugins": ["oh-my-opencode"]`
- 定义了 providers 和 models
- 配置了 task routing

### 2. .opencode/oh-my-opencode.json（插件配置）
- 定义了 agents（Sisyphus, Prometheus, Oracle, Librarian）
- 配置了 background agents
- 启用了 productivity features

---

## 🎉 现在可以开始了！

复制这一行到 PowerShell：

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'; Get-Content .env | ForEach-Object { if ($_ -match "^\s*([^#][^=]+)=(.*)$") { $name = $matches[1].Trim(); $value = $matches[2].Trim(); [Environment]::SetEnvironmentVariable($name, $value, "Process") } }; opencode --config opencode.json
```

然后在 OpenCode 中输入（记得加 `ulw`）：

```
ulw Design lesson: Unit 1 Goldilocks, 五年级, 译林版, 9-stage workflow
```

**就这么简单！** 🚀

---

## 参考资料

- [Oh My OpenCode GitHub](https://github.com/code-yeongyu/oh-my-opencode)
- [安装指南](https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.md)
- [功能文档](https://github.com/code-yeongyu/oh-my-opencode#features)
- [配置文档](https://github.com/code-yeongyu/oh-my-opencode#configuration)
