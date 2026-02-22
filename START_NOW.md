# 🚀 最简单的启动方式

## 当前项目使用 Oh My OpenCode

**Sisyphus 作为主调度器，管理所有教学设计 agents**

---

## 📋 3步启动（最简单）

### 在新的终端窗口中运行：

### 步骤1：进入项目目录

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
```

### 步骤2：启动 Oh My OpenCode

```powershell
.\.opencode\start-ohmyopencode.bat
```

**或者直接运行**：

```powershell
opencode
```

### 步骤3：输入任务（使用 ulw 激活 Sisyphus）

```
ulw Design lesson: Unit 1 Goldilocks and the three bears, 五年级, 译林版

Execute 9-stage workflow, pause at stage 4 for confirmation.
```

---

## 🎯 就这么简单！

**Sisyphus 会自动**：
- ✅ 分析项目结构（读取 AGENTS.md）
- ✅ 扫描教学材料（materials/ 文件夹）
- ✅ 按 9 个阶段依次执行
- ✅ 在阶段 4 暂停等待确认
- ✅ 自动选择最佳 AI 模型
- ✅ 生成所有文档
- ✅ 记录日志到 state/LOG.md

---

## 📊 查看进度

在另一个终端窗口运行：

```powershell
.\.opencode\check-progress.bat
```

**或 PowerShell 版本**：

```powershell
.\.opencode\check-progress.ps1
```

---

## 💡 快速示例

### 完整命令（复制粘贴）

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
.\.opencode\start-ohmyopencode.bat
```

然后在 OpenCode 中输入：

```
ulw Design lesson: Unit 1 Goldilocks, 五年级, 译林版, 9-stage workflow
```

---

## ✨ 什么是 `ulw`？

`ulw` = **ultrawork** 的缩写

这会激活 **Sisyphus Agent**（西西弗斯代理），他是 Oh My OpenCode 的核心调度器。

**Sisyphus 的能力**：
- 🎯 自动任务分解和执行
- 🧠 智能模型选择
- 📋 TODO 列表强制执行
- 🔄 错误处理和重试
- 📊 进度跟踪和日志

---

## 🔄 工作流程

```
用户输入 → Sisyphus 解析 → 创建 TODO
    ↓
Stage 1: 材料审核 (Gemini Pro 1.5)
    ↓
Stage 2: 课程分析 (Claude 3.5 Sonnet)
    ↓
Stage 3: 内容设计 (Claude 3.5 Sonnet)
    ↓
Stage 4: 大任务建议 (暂停等待确认) ⏸️
    ↓
Stage 5: 活动设计 (Claude 3.5 Sonnet)
    ↓
Stage 6: 资源协调 (Claude 3 Haiku - 快速)
    ↓
Stage 7: 评估设计 (Claude 3.5 Sonnet)
    ↓
Stage 8: 质量审核 (Claude 3.5 Sonnet)
    ↓
Stage 9: 打包发布 (Claude 3 Haiku - 快速)
    ↓
完成！✅
```

---

## 📁 生成的文件

### 过程文档（state/）
- ✅ MATERIAL_AUDIT.md - 材料审核
- ✅ CURRICULUM_ANALYSIS.md - 课程分析
- ✅ CONTENT_DESIGN.md - 内容设计
- ✅ BIG_TASK_PROPOSAL.md - 大任务建议
- ✅ ACTIVITY_DESIGN.md - 活动设计
- ✅ RESOURCE_LIST.md - 资源清单
- ✅ ASSESSMENT_DESIGN.md - 评估设计
- ✅ QUALITY_REVIEW.md - 质量审核
- ✅ LOG.md - 工作日志

### 最终交付（draft/）
- ⭐ **lesson_plan.md** - 完整教案（主文件）
- ⭐ student_preview_guide.md - 学生预习清单
- ⭐ homework_sheet.md - 家庭作业纸
- ✅ PACKAGE_CHECKLIST.md - 交付清单
- ✅ USAGE_GUIDE.md - 使用说明

---

## 🆚 对比传统方式

### ❌ 传统方式（繁琐）

```powershell
python tools/run_stage.py --stage material_intake
python tools/run_stage.py --stage curriculum_analysis
python tools/run_stage.py --stage content_design
# ... 还要运行 6 次
```

### ✅ 使用 Sisyphus（简单）

```powershell
ulw Design lesson: [主题], [年级], [教材]
```

**一行命令，自动完成所有！**

---

## 📚 更多信息

- 系统架构：`AGENTS.md`
- 详细配置：`CORRECT_STARTUP_PROCESS.md`
- Oh My OpenCode：[GitHub](https://github.com/code-yeongyu/oh-my-opencode)
- OpenCode 文档：[opencode.ai](https://opencode.ai)

---

## 🎉 现在就开始！

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
.\.opencode\start-ohmyopencode.bat
```

然后输入：

```
ulw Design lesson: Unit 1 Goldilocks, 五年级, 译林版
```

**就是这么简单！** 🚀
