# ⚡ 快速参考卡
## 一页纸搞定所有操作

---

## 🚀 启动新项目（三步）

```powershell
# 1. 进入项目目录
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down

# 2. 启动教学设计
.\start-lesson-design.ps1 "主题" "年级" "教材"

# 3. 按任意键开始，然后等待完成
```

### 实际示例

```powershell
# 译林版五年级
.\start-lesson-design.ps1 "Unit 1 Goldilocks" "五年级" "译林版"

# 人教版PEP三年级
.\start-lesson-design.ps1 "Unit 2 Colours" "三年级" "人教版PEP"

# 外研版四年级
.\start-lesson-design.ps1 "Module 3 My School" "四年级" "外研版"
```

---

## ⏸️ 用户确认点（重要！）

当看到这个提示时：

```
📋 核心大任务建议

Activity Designer 建议本节课的核心大任务为：
"续写 Goldilocks 的故事，并进行小组角色扮演"

请选择：
1. ✅ 确认使用此大任务
2. ✏️ 修改大任务
3. 🔄 选择备选方案

你的选择：_
```

**你要做什么**：
1. 查看 `state\BIG_TASK_PROPOSAL.md` 了解详情
2. 输入 `1`（确认）或 `2`（修改）或 `3`（备选）
3. 按回车

**最常用**：直接输入 `1` 然后回车

---

## 📁 查看结果

```powershell
# 查看主教案（最重要）
notepad draft\lesson_plan.md

# 查看预习清单
notepad draft\student_preview_guide.md

# 查看作业纸
notepad draft\homework_sheet.md

# 查看所有文件
explorer draft\
```

---

## 🔍 监控进度（可选）

在另一个 PowerShell 窗口：

```powershell
# 实时日志
Get-Content state\LOG.md -Wait -Tail 50

# 查看状态
cat state\STATUS.yaml

# 查看成本
cat state\cost.log
```

---

## 📚 上传教材（推荐，可选）

```powershell
# 复制教材到项目
Copy-Item "D:\你的教材路径.pdf" "materials\textbooks\"

# 复制课程标准
Copy-Item "D:\课程标准.docx" "materials\standards\"

# 然后正常启动项目
.\start-lesson-design.ps1 "主题" "年级" "教材"
```

---

## ⏱️ 时间线

| 阶段 | 时间 | 动作 |
|------|------|------|
| 启动 | 30秒 | 按任意键 |
| 材料审核 | 1-2分钟 | 自动 |
| 课程分析 | 1-2分钟 | 自动 |
| 内容设计 | 2-3分钟 | 自动 |
| **确认点** | **30秒** | **输入1** |
| 活动设计 | 2-3分钟 | 自动 |
| 资源协调 | 1分钟 | 自动 |
| 评估设计 | 1-2分钟 | 自动 |
| 质量审核 | 1-2分钟 | 自动 |
| 打包发布 | 1-2分钟 | 自动 |
| **总计** | **10-20分钟** | - |

---

## 💰 成本

- 单次设计：**$0.60-$0.80**
- 10次设计：**$6-$8**
- 100次设计：**$60-$80**

---

## 🐛 常见问题

### Q: API 连接失败？
```powershell
# 检查 API Key
notepad .env
# 确保 OPENROUTER_API_KEY=sk-or-v1-真实密钥
```

### Q: 流程卡住不动？
- 可能在等待用户确认
- 查看屏幕提示，输入 `1` 并回车

### Q: 想重新开始？
```powershell
# 清理旧文件
Remove-Item state\*.md -Force
Remove-Item draft\*.md -Force

# 重新启动
.\start-lesson-design.ps1 "主题" "年级" "教材"
```

### Q: 想用更便宜的模型？
编辑 `.env` 文件：
```
DEFAULT_MODEL=openrouter/anthropic/claude-3-haiku
LONG_CONTEXT_MODEL=openrouter/google/gemini-flash-1.5
```
成本降至 **$0.30/次**

---

## 📖 完整文档

| 文档 | 用途 |
|------|------|
| `QUICK_START_NEW_PROJECT.md` | 详细的启动指南 |
| `README_OPENCODE.md` | 完整使用手册 |
| `INSTALLATION_COMPLETE.md` | 安装总结 |
| 本文档 | 快速参考 |

---

## 🎯 现在就开始！

```powershell
.\start-lesson-design.ps1 "Unit 1 Goldilocks" "五年级" "译林版"
```

**提示**：
1. 启动后按任意键
2. 在确认点输入 `1`
3. 等待10-15分钟
4. 查看 `draft\lesson_plan.md`

---

**🎉 就这么简单！**
