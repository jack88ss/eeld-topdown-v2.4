# 📋 项目信息

## 项目名称
Elementary English Lesson Designer (EELD)
小学英语教学设计智能代理系统

## 版本
2.5.0 - Oh My OpenCode 版本

## 架构
OpenCode + Oh My OpenCode 插件

---

## 🏗️ 系统架构

### 主调度器
**Sisyphus** (Oh My OpenCode 核心 agent)
- 负责任务分解和调度
- 自动选择最佳 AI 模型
- 强制执行 TODO 列表
- 处理错误和重试

### Sub-Agents（8个）
1. **Orchestrator** (姜子牙) - 流程管理和材料审核
2. **Curriculum Analyst** - 课程分析
3. **Content Designer** - 内容设计
4. **Activity Designer** - 活动设计
5. **Resource Coordinator** - 资源协调
6. **Assessment Expert** - 评估设计
7. **Quality Reviewer** - 质量审核
8. **Package Publisher** - 打包发布

---

## 📊 工作流程

9个阶段，自动执行：

```
Stage 1: 材料审核 (Gemini Pro 1.5)
Stage 2: 课程分析 (Claude 3.5 Sonnet)
Stage 3: 内容设计 (Claude 3.5 Sonnet)
Stage 4: 大任务建议 (暂停确认) ⏸️
Stage 5: 活动设计 (Claude 3.5 Sonnet)
Stage 6: 资源协调 (Claude 3 Haiku)
Stage 7: 评估设计 (Claude 3.5 Sonnet)
Stage 8: 质量审核 (Claude 3.5 Sonnet)
Stage 9: 打包发布 (Claude 3 Haiku)
```

---

## 🚀 使用方法

### 最简单方式

```powershell
# 1. 启动
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
.\.opencode\start-ohmyopencode.bat

# 2. 输入任务
ulw Design lesson: [主题], [年级], [教材]
```

### 查看进度

```powershell
.\.opencode\check-progress.bat
```

---

## 📁 项目结构

```
eeld-top-down/
├── .opencode/                    # OpenCode 配置和脚本
│   ├── start-ohmyopencode.bat   # 启动脚本
│   ├── check-progress.bat       # 进度查看
│   └── oh-my-opencode.json      # Oh My OpenCode 配置
│
├── state/                        # 过程文档（9个阶段）
│   ├── MATERIAL_AUDIT.md
│   ├── CURRICULUM_ANALYSIS.md
│   ├── CONTENT_DESIGN.md
│   ├── BIG_TASK_PROPOSAL.md
│   ├── ACTIVITY_DESIGN.md
│   ├── RESOURCE_LIST.md
│   ├── ASSESSMENT_DESIGN.md
│   ├── QUALITY_REVIEW.md
│   └── LOG.md
│
├── draft/                        # 最终交付物
│   ├── lesson_plan.md           # 完整教案 ⭐
│   ├── student_preview_guide.md # 预习清单
│   ├── homework_sheet.md        # 作业纸
│   ├── PACKAGE_CHECKLIST.md
│   └── USAGE_GUIDE.md
│
├── materials/                    # 教学材料输入
│   ├── textbooks/               # 教材
│   ├── standards/               # 课程标准
│   └── reference/               # 参考资料
│
├── assets/                       # 教学资源
│
├── opencode.json                 # OpenCode 主配置
├── .env                          # 环境变量（API keys）
│
└── 文档/
    ├── START_NOW.md             # 立即开始（推荐）
    ├── QUICK_START.md           # 快速指南
    ├── AGENTS.md                # 系统架构详解
    ├── CORRECT_STARTUP_PROCESS.md  # 详细配置
    └── PROJECT_INFO.md          # 本文件
```

---

## 🎯 核心特性

### 1. 自动化
- ✅ 一行命令启动
- ✅ 自动任务分解
- ✅ 自动模型选择
- ✅ 自动执行所有阶段

### 2. 智能化
- ✅ 根据任务类型选择最佳模型
- ✅ 长文本用 Gemini Pro 1.5
- ✅ 复杂分析用 Claude 3.5 Sonnet
- ✅ 快速整理用 Claude 3 Haiku

### 3. 可靠性
- ✅ TODO 强制执行
- ✅ 错误自动重试
- ✅ 完整日志记录
- ✅ 进度实时追踪

### 4. 用户友好
- ✅ 简单启动脚本
- ✅ 进度查看工具
- ✅ 清晰的文档结构
- ✅ 暂停确认机制

---

## 🔧 技术栈

- **OpenCode**: 开源 AI 代码助手框架
- **Oh My OpenCode**: 增强插件（Sisyphus 调度器）
- **AI Models**:
  - Google Gemini Pro 1.5 (长上下文)
  - Anthropic Claude 3.5 Sonnet (推理)
  - Anthropic Claude 3 Haiku (快速)
- **Provider**: OpenRouter (统一 API 网关)
- **Runtime**: Node.js / Bun

---

## 📚 配置文件

### 1. opencode.json
- 定义 AI providers 和 models
- 启用 oh-my-opencode 插件
- 配置工具和任务路由

### 2. .opencode/oh-my-opencode.json
- 配置 Sisyphus 和 sub-agents
- 启用 background agents
- 配置 productivity features

### 3. .env
- OpenRouter API key
- 其他环境变量

---

## 🎓 教学理念

本系统基于 **"任务驱动、自上而下学习法"**：

1. **真实任务**：学生完成有意义的真实任务
2. **完整过程**：从理解到产出的完整学习过程
3. **有形成果**：可展示、可分享的学习成果
4. **交际目的**：真实的语言交际需求
5. **单一聚焦**：核心大任务单一聚焦

---

## 📈 性能指标

- **执行时间**：约 12-15 分钟
- **成本**：约 $0.5-1.0 per lesson
- **模型调用**：15-20 次
- **文档生成**：13 个文件

---

## 🆚 版本对比

### v1.0 - 传统脚本版本
- ❌ 手动运行每个阶段
- ❌ 手动选择模型
- ❌ 无自动重试
- ⚠️ 容易遗漏步骤

### v2.5 - Oh My OpenCode 版本（当前）
- ✅ 自动执行所有阶段
- ✅ 智能模型选择
- ✅ 自动错误处理
- ✅ TODO 强制执行
- ✅ 一行命令启动

---

## 🔗 相关链接

- [Oh My OpenCode GitHub](https://github.com/code-yeongyu/oh-my-opencode)
- [OpenCode 官方网站](https://opencode.ai)
- [OpenCode GitHub](https://github.com/anomalyco/opencode)
- [OpenRouter API](https://openrouter.ai)

---

## 👥 开发团队

- **架构设计**：基于 Oh My OpenCode 的 Sisyphus 架构
- **教学理念**：任务驱动、自上而下学习法
- **AI 模型选择**：根据任务特性优化

---

## 📝 更新日志

### v2.5.0 (2026-01-19)
- ✅ 迁移到 Oh My OpenCode
- ✅ 引入 Sisyphus 主调度器
- ✅ 重构 AGENTS.md 架构文档
- ✅ 创建简化启动脚本
- ✅ 创建进度查看工具
- ✅ 优化文档结构

### v2.4.0 (之前)
- 基于传统脚本的版本
- 手动执行各个阶段

---

## 🎉 快速开始

详见：`START_NOW.md`

```powershell
cd 'C:\Users\Administrator\Desktop\myproject\eeld-top-down'
.\.opencode\start-ohmyopencode.bat
```

然后输入：

```
ulw Design lesson: [主题], [年级], [教材]
```

**就这么简单！** 🚀
