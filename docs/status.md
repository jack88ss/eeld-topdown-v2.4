# 小学英语教学设计流程状态

更新此文件以概览阶段、任务状态与守门条件。需与 `state/STATUS.yaml`、`state/LOG.md` 一致，并写明最近更新时间。

**最近更新**：2026-02-03T00:00:00Z | 完成课程分析与内容设计，核心大任务待确认

## 当前阶段
- `state/STATUS.yaml` → current_stage: **design**
- 系统状态：**推进中**，等待核心大任务确认
- **当前任务**：big_task_proposal（用户确认点）

## 上次完成任务
- 主题：Colors（颜色）
- 年级：三年级
- 教材：人教版PEP
- 状态：✅ 已完成（2026-01-17T05:40:00Z）
- 交付物：draft/lesson_plan.md（9页完整教案）

## 任务摘要
| 任务ID | 阶段 | 状态 | 负责人 | 输出文档 |
|--------|------|------|--------|----------|
| **material_intake** | **plan** | **done** | **orchestrator** | **state/MATERIAL_AUDIT.md** ⭐新增 |
| curriculum_analysis | plan | done | curriculum_analyst | state/CURRICULUM_ANALYSIS.md |
| content_design | design | done | content_designer | state/CONTENT_DESIGN.md |
| **big_task_proposal** | **design** | **todo** | **activity_designer** | **state/BIG_TASK_PROPOSAL.md** ⭐确认点 |
| activity_design | design | blocked | activity_designer | state/ACTIVITY_DESIGN.md |
| resource_coordination | resource | blocked | resource_coordinator | state/RESOURCE_LIST.md |
| assessment_design | assessment | blocked | assessment_expert | state/ASSESSMENT_DESIGN.md |
| quality_review | review | blocked | quality_reviewer | state/QUALITY_REVIEW.md |
| package_publish | publish | blocked | package_publisher | draft/lesson_plan.md |

## 代理团队状态
| 代理 | 角色 | 状态 |
|------|------|------|
| Orchestrator | 流程总指挥（姜子牙） | ✅ 在线 |
| Curriculum Analyst | 课程分析师 | 待命 |
| Content Designer | 内容设计师 | 待命 |
| Activity Designer | 活动设计师 | 待命 |
| Resource Coordinator | 资源协调员 | 待命 |
| Assessment Expert | 评估专家 | 待命 |
| Quality Reviewer | 质量审核员 | 待命 |
| Package Publisher | 发布专家 | 待命 |

## 守门条件追踪
- **材料审核**：orchestrator 必须完成材料扫描和审核，至少有教材或课程标准 ⭐新增
- **课程分析**：curriculum_analyst 必须基于上传材料完成分析，识别重难点
- **内容设计**：content_designer 的设计必须紧扣教学目标和教材内容
- **活动设计**：activity_designer 的活动必须层次分明、可操作
- **资源准备**：resource_coordinator 必须确保资源清单完整且可获取
- **评估设计**：assessment_expert 的评估必须与教学目标和课程标准对齐
- **质量审核**：quality_reviewer 必须确认所有审核项通过
- **打包发布**：package_publisher 必须生成完整可用的教案文档

## 启动新任务

### 步骤1：上传教学材料 ⭐新增
将教学材料上传到对应文件夹：
- 📚 **教材** → `materials/textbooks/`（学生用书、教师用书）
- 📋 **课程标准** → `materials/standards/`
- 📖 **参考资料** → `materials/reference/`

支持格式：PDF、Word、TXT、Markdown

### 步骤2：启动设计流程
使用命令：`/start-lesson-design <主题> <年级> <教材>`

示例：
- `/start-lesson-design Animals 四年级 人教版PEP`
- `/start-lesson-design My_Family 三年级 外研版`

### 新工作流程
```
材料审核 → 课程分析 → 内容设计 → 活动设计 → 
资源协调 → 评估设计 → 质量审核 → 打包发布
```

> 每次阶段变更后会自动更新本文件。详细执行日志见 `state/LOG.md`。
