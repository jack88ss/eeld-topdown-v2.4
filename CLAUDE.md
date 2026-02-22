# 项目章程（小学英语教学设计）

## 目标

生成完整的小学英语教学设计，基于用户上传的真实教材和课程标准，交付物为 `draft/lesson_plan.md`（完整教案）+ 教学资源（`assets/`）+ 评估工具。

## 核心特性 ⭐v2.1新增

### 材料上传功能
- 支持上传教材（学生用书、教师用书）到 `materials/textbooks/`
- 支持上传课程标准到 `materials/standards/`
- 支持上传参考资料到 `materials/reference/`
- 支持格式：PDF、Word (.doc, .docx)、TXT、Markdown
- 自动材料审核与内容提取

## 多代理分工

0. **orchestrator** — 流程总指挥，扫描并审核用户上传的教学材料，生成 `state/MATERIAL_AUDIT.md`
1. **curriculum_analyst** — 基于真实材料分析教学目标、学生特点、重难点，更新 `state/CURRICULUM_ANALYSIS.md`
2. **content_designer** — 设计知识点呈现方式和讲解策略，更新 `state/CONTENT_DESIGN.md`
3. **activity_designer** — 设计课堂活动、游戏、互动环节，更新 `state/ACTIVITY_DESIGN.md`
4. **resource_coordinator** — 整理教学资源（PPT、图片、音频等），更新 `state/RESOURCE_LIST.md`、`state/SOURCES.md`
5. **assessment_expert** — 设计评估方式和练习题，更新 `state/ASSESSMENT_DESIGN.md`
6. **quality_reviewer** — 审核教学设计质量，记录于 `state/QUALITY_REVIEW.md`、`state/ITERATIONS.md`
7. **package_publisher** — 打包生成完整教案，生成 `draft/lesson_plan.md`、`draft/PACKAGE_CHECKLIST.md`、`draft/USAGE_GUIDE.md`

## 状态机

`state/STATUS.yaml` 维护阶段与守门条件；`/start-lesson-design` 负责解析并调度。

工作流程：
```
材料审核 → 课程分析 → 内容设计 → 活动设计 → 
资源协调 → 评估设计 → 质量审核 → 打包发布
```

## 事实源

- **用户材料**：`materials/` 目录（教材、课程标准、参考资料）⭐新增
- **过程文档**：`state/` 目录构成单一事实来源
- **示例参考**：`samples/lesson-designs/` 提供优秀案例
- **修改原则**：所有修改须追加而非覆盖历史

## 核心规范

### 基本要求
- 基于用户上传的真实教材内容 ⭐新增
- 严格对齐课程标准 ⭐新增
- 符合小学英语课程标准
- 基于儿童认知规律
- 遵循有效教学原则

### 内心独角戏系统
每个代理必须在 `state/LOG.md` 中记录剧本式的工作过程，包括登场介绍、观察输入、内心独白、决策过程、执行动作五幕（详见 `AGENT_MONOLOGUE_SYSTEM.md`）。

## 资源策略

### 数字资源
- PPT结构大纲
- 图片素材
- 音频文件
- 视频资源

### 实体教具
- 单词卡片
- 图片卡片
- 实物道具
- 板书设计

### 资源管理
- 优先使用免费教育资源
- 注明版权和来源
- 在 `state/SOURCES.md` 记录所有外部资源来源
- 在 `materials/` 存放用户上传的教学材料 ⭐新增

## 教学设计要求

### 符合课程标准
- 基于《义务教育英语课程标准》
- 对齐课程标准的年级目标 ⭐新增
- 参考教师用书的教学建议 ⭐新增

### 三维目标
- 知识与技能
- 过程与方法
- 情感态度与价值观

### 五步教学
- Warm-up（热身）
- Presentation（呈现）
- Practice（操练）
- Production（输出）
- Summary（总结）

### 时间控制
- 一般40分钟
- 各环节时间分配合理

### 活动设计
- 层次性（机械→有意义→交际）
- 趣味性
- 有效性

### 差异化
- 考虑不同水平学生的需求

## 质量守门条件

### 材料审核阶段 ⭐新增
- **Orchestrator** 必须完成材料扫描和审核
- 至少有教材或课程标准之一
- 材料审核报告完整
- 在 `state/LOG.md` 记录审核过程

### 课程分析阶段
- **Curriculum Analyst** 必须基于上传材料完成分析
- 教学目标明确、可测量、可达成
- 重难点清晰，符合教材内容 ⭐新增
- 与课程标准对齐 ⭐新增

### 其他阶段
- **Content Designer**：内容准确、地道、适合学生水平
- **Activity Designer**：活动有效、可行、时间合理
- **Resource Coordinator**：资源完整、易获取、版权合规
- **Assessment Expert**：评估多元、对齐目标、可操作
- **Quality Reviewer** 和 **Curriculum Analyst** 必须在 `state/LOG.md` 签名确认

## 日志要求

### 剧本式记录+交接验证
参考 `AGENT_HANDOFF_PROTOCOL.md`

### 每个代理必须
- 记录五幕独角戏（200-500字）
- 交接清单
- 责任签名

### 交接验证
- 必须100%通过
- 不允许TODO/待定/模糊项

### 返工机制
- 问题定位 → 责任代理 → REWORK状态 → 重新执行

## 禁止事项

- ❌ 不得生成其他格式（除Markdown外）
- ❌ 不得虚构教学内容或资源来源
- ❌ 不得覆盖他人日志或删除历史记录
- ❌ 不得使用模糊词：约/大概/左右/可能/建议/或许/待定/TODO（除待办清单）
- ❌ 不得跳过交接验证，不得在验证失败时继续
- ❌ 不得忽略用户上传的教学材料 ⭐新增

## 守门条件示例

- **G0（material）**：`MATERIAL_AUDIT.md` 完成，材料审核通过 ⭐新增
- **G1（plan）**：`CURRICULUM_ANALYSIS.md` 完成，基于材料分析，教学目标明确，重难点清晰
- **G2（design）**：`CONTENT_DESIGN.md`、`ACTIVITY_DESIGN.md` 完成，内容和活动设计科学有效
- **G3（resource）**：`RESOURCE_LIST.md` 完成，资源清单完整，来源记录于 `SOURCES.md`
- **G4（assessment）**：`ASSESSMENT_DESIGN.md` 完成，评估方式多元且与目标对齐
- **G5（review）**：Quality Reviewer 在 `state/LOG.md` 签字确认无阻塞问题
- **Publish**：Package Publisher 生成完整教案，`STATUS.yaml` 设为 `publish` 或 `done`

## 适配 Claude Skills

本系统设计为标准的 Claude Skill：

### 独立使用
通过 `/start-lesson-design` 命令调用

### 组合使用
可与图片生成、音频合成、文档翻译等 Skills 组合

### 状态持久化
所有状态保存在 `state/` 目录，支持断点续传和多会话

### 权限管理
通过 `.claude/settings.json` 控制文件访问和工具使用权限

### 扩展性
可轻松添加新代理或修改工作流

## 版本信息

- **当前版本**：v2.1.0
- **最后更新**：2026-01-17
- **主要特性**：基于真实教材的教学设计生成系统

---

遵循以上约束，可确保每份教学设计符合专业标准，具备科学性和可操作性，并能充分利用用户提供的真实教学材料。
