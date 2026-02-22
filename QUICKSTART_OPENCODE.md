# OpenCode 快速启动指南
## 5分钟开始使用教学设计系统

---

## 🎯 目标

让你在5分钟内完成部署并生成第一份教学设计。

---

## ✅ 检查清单

在开始前，确保你已经：
- [ ] 安装了 OpenCode
- [ ] 安装了 Oh My OpenCode  
- [ ] 获取了 OpenRouter API Key
- [ ] 准备好教材文件

---

## 📋 步骤1：安装依赖（2分钟）

打开 PowerShell，执行：

```powershell
# 安装 OpenCode
npm install -g opencode

# 安装 Oh My OpenCode
npm install -g oh-my-opencode

# 验证安装
opencode --version
oh-my-opencode --version
```

看到版本号说明安装成功！✅

---

## 🔑 步骤2：获取 API Key（1分钟）

1. 访问 https://openrouter.ai/keys
2. 注册/登录账号
3. 点击 "Create Key" 创建新密钥
4. 复制密钥（格式：`sk-or-v1-...`）

**重要**：保存好密钥，它只显示一次！

---

## ⚙️ 步骤3：配置项目（1分钟）

在项目目录运行快速部署脚本：

```powershell
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down
.\setup.ps1
```

脚本会自动：
- ✅ 检查环境
- ✅ 创建 `.env` 文件
- ✅ 创建必要目录
- ✅ 验证配置文件

完成后，编辑 `.env` 文件：

```bash
# 打开 .env 文件
notepad .env

# 找到这一行：
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# 替换为你的实际密钥：
OPENROUTER_API_KEY=sk-or-v1-实际的密钥
```

保存并关闭。

---

## 📚 步骤4：上传教材（30秒）

将教材文件放到对应文件夹：

```
materials/
├── textbooks/
│   └── 译林版五上英语电子课本.pdf  ← 放这里
├── standards/
│   └── 课程标准.docx                ← 放这里（可选）
└── reference/
    └── 参考资料.pdf                 ← 放这里（可选）
```

**最少要求**：至少放一个教材文件。

---

## 🚀 步骤5：启动流程（30秒）

运行启动脚本：

```powershell
.\start-lesson-design.ps1 "Unit 1 Goldilocks" "五年级" "译林版"
```

**参数说明：**
- 第1个参数：教学主题（如 "Unit 1 Goldilocks"）
- 第2个参数：年级（如 "五年级"）
- 第3个参数：教材版本（如 "译林版"）

按回车，系统开始工作！🎉

---

## 👀 步骤6：监控进度（可选）

在另一个 PowerShell 窗口查看实时日志：

```powershell
# 查看日志（实时更新）
Get-Content state/LOG.md -Wait -Tail 50

# 查看状态
cat state/STATUS.yaml

# 查看成本
cat state/cost.log
```

---

## ⏸️ 用户确认点

当系统执行到**核心大任务建议**阶段时，会暂停并显示：

```
📋 核心大任务建议

Activity Designer 建议本节课的核心大任务为：
"续写Goldilocks的故事，并进行角色扮演"

详细信息请查看：state/BIG_TASK_PROPOSAL.md

请选择：
1. ✅ 确认使用此大任务
2. ✏️ 修改大任务（请提供修改内容）
3. 🔄 选择备选方案

你的选择：
```

**你需要：**
- 打开 `state/BIG_TASK_PROPOSAL.md` 查看详细建议
- 在控制台输入 `1`、`2` 或 `3` 并回车
- 系统会记录你的选择并继续执行

---

## 📦 步骤7：查看结果

完成后（约5-10分钟），在 `draft/` 文件夹查看生成的文档：

```
draft/
├── lesson_plan.md               # 📘 完整教案（重点！）
├── student_preview_guide.md     # 📝 学生预习清单
├── homework_sheet.md            # ✏️ 家庭作业纸
├── PACKAGE_CHECKLIST.md         # ✅ 交付物清单
└── USAGE_GUIDE.md               # 📖 使用说明
```

**重点查看：** `lesson_plan.md` - 这是最核心的教案文档。

---

## 💡 常见问题速查

### ❌ 错误：`opencode: command not found`

**原因**：OpenCode 未安装或未添加到 PATH。

**解决**：
```powershell
npm install -g opencode
# 重启 PowerShell
```

---

### ❌ 错误：`API Error: 401 Unauthorized`

**原因**：API Key 未配置或错误。

**解决**：
1. 检查 `.env` 文件中的 `OPENROUTER_API_KEY`
2. 确保密钥格式正确（`sk-or-v1-...`）
3. 重新启动流程

---

### ❌ 错误：`Request exceeds the maximum size`

**原因**：PDF 文件太大（超过 24MB）。

**解决**：系统会自动切换到 Gemini Pro 1.5 模型。如果仍然失败：
1. 检查 OpenRouter API Key 是否支持 Gemini
2. 尝试将PDF分割成更小的文件
3. 查看 `state/LOG.md` 了解详细错误

---

### ⏸️ 系统在等待用户确认时卡住了

**原因**：这是正常的！系统设计为在核心大任务提出后暂停。

**解决**：
1. 查看 `state/BIG_TASK_PROPOSAL.md`
2. 在控制台输入 `1`、`2` 或 `3`
3. 按回车继续

---

## 🎓 下一步

成功生成第一份教学设计后，你可以：

1. **查看完整文档**：`README_OPENCODE.md`
2. **学习高级功能**：自定义代理、工作流、hooks
3. **优化成本**：调整模型选择策略
4. **使用 GPT-5.2-Codex**：生成自动化脚本

---

## 📞 需要帮助？

- 📖 查看完整文档：`README_OPENCODE.md`
- 🐛 报告问题：[GitHub Issues](https://github.com/your-repo/issues)
- 💬 加入讨论：[Discord](https://discord.gg/your-server)
- 📧 联系我们：your-email@example.com

---

**🎉 恭喜！你已经完成了快速启动！**

现在开始享受智能教学设计系统带来的便利吧！
