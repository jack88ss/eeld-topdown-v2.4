# 🚀 极简快速启动指南

## 3步启动任务

### 步骤1：进入目录 + 加载环境变量（1分钟）
```powershell
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down
Get-Content .env | ForEach-Object { if ($_ -match "^\s*([^#][^=]+)=(.*)$") { $name = $matches[1].Trim(); $value = $matches[2].Trim(); [Environment]::SetEnvironmentVariable($name, $value, "Process") } }
```

### 步骤2：启动 OpenCode（30秒）
```powershell
opencode --config opencode.json
```

### 步骤3：输入任务（1分钟）
在 OpenCode 提示符 `>` 后输入：

```
设计小学英语教案：主题 [主题名]，[年级]，[教材版本]，按9阶段执行（材料审核→课程分析→内容设计→大任务建议→活动设计→资源协调→评估设计→质量审核→打包发布），阶段4暂停等待确认。
```

**实际例子**：
```
设计小学英语教案：主题 Unit 1 Goldilocks and the three bears，五年级，译林版，按9阶段执行（材料审核→课程分析→内容设计→大任务建议→活动设计→资源协调→评估设计→质量审核→打包发布），阶段4暂停等待确认。
```

---

## 执行中的操作

**阶段4暂停时**：OpenCode会显示大任务建议，输入：
- `1` 然后回车（确认）
- 或修改建议

**等待完成**：10-15分钟自动执行

**查看结果**：
```powershell
notepad draft\lesson_plan.md
```

---

## 完整版启动命令（一行复制）

```powershell
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down; Get-Content .env | ForEach-Object { if ($_ -match "^\s*([^#][^=]+)=(.*)$") { $name = $matches[1].Trim(); $value = $matches[2].Trim(); [Environment]::SetEnvironmentVariable($name, $value, "Process") } }; opencode --config opencode.json
```

复制这一行到 PowerShell，回车，然后输入任务即可！

---

## 🎯 就这么简单！

1️⃣ 复制上面的一行命令 → 回车  
2️⃣ 输入任务描述 → 回车  
3️⃣ 等待完成 → 查看结果
