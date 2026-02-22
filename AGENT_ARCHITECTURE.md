# 多代理教学设计架构

## 总览

系统以 `/start-lesson-design` 为唯一入口，按照 `state/STATUS.yaml` 状态机调度八个专业代理，基于用户上传的真实教材和课程标准，最终交付完整的小学英语教学设计（`draft/lesson_plan.md`）与教学资源。

## 核心特性 ⭐v2.1新增

### 材料上传功能
- 支持上传教材（学生用书、教师用书）
- 支持上传课程标准
- 支持上传参考资料
- 支持格式：PDF、Word、TXT、Markdown
- 自动材料审核与内容提取

## 代理职责

| 代理 | 职责 | 主要产出 |
|------|------|----------|
| **orchestrator** | 流程总指挥，材料审核 ⭐新增 | `state/MATERIAL_AUDIT.md` |
| **curriculum_analyst** | 基于材料分析教学目标、学生特点、重难点 | `state/CURRICULUM_ANALYSIS.md` |
| **content_designer** | 设计知识点呈现方式和讲解策略 | `state/CONTENT_DESIGN.md` |
| **activity_designer** | 设计课堂活动、游戏、互动环节 | `state/ACTIVITY_DESIGN.md` |
| **resource_coordinator** | 整理教学资源（PPT、图片、音频） | `state/RESOURCE_LIST.md`、`state/SOURCES.md` |
| **assessment_expert** | 设计评估方式和练习题 | `state/ASSESSMENT_DESIGN.md` |
| **quality_reviewer** | 审核教学设计质量 | `state/QUALITY_REVIEW.md`、`state/ITERATIONS.md` |
| **package_publisher** | 打包生成完整教案 | `draft/lesson_plan.md` 等 |

## 工作流程

0. **材料审核** ⭐新增：orchestrator 扫描并审核用户上传的教学材料
1. **课程分析**：curriculum_analyst 基于真实材料分析教学目标和学生特点
2. **内容设计**：content_designer 设计知识点呈现方式
3. **活动设计**：activity_designer 设计课堂活动和互动
4. **资源协调**：resource_coordinator 整理教学资源清单
5. **评估设计**：assessment_expert 设计评估和练习题
6. **质量审核**：quality_reviewer 全面审核设计质量
7. **打包发布**：package_publisher 生成完整教案文档

## 关键文件

### 输入材料 ⭐新增
- `materials/textbooks/`：用户上传的教材
- `materials/standards/`：课程标准
- `materials/reference/`：参考资料

### 状态与过程
- `state/STATUS.yaml`：状态机与守门条件
- `state/LOG.md`：流程日志与追踪
- `state/MATERIAL_AUDIT.md`：材料审核报告 ⭐新增
- `state/CURRICULUM_ANALYSIS.md` - `ASSESSMENT_DESIGN.md`：各阶段设计文档
- `state/QUALITY_REVIEW.md`：质量审核报告

### 最终输出
- `draft/lesson_plan.md`：最终教案
- `assets/`：教学资源文件

## 设计原则

### 1. 专业性
- 基于真实教材内容 ⭐新增
- 严格对齐课程标准 ⭐新增
- 符合《义务教育英语课程标准》
- 基于语言学习规律和儿童认知特点
- 遵循有效教学原则

### 2. 科学性
- 教学目标明确可测
- 内容准确地道
- 活动设计有效
- 评估科学合理

### 3. 可操作性
- 流程清晰，教师易于理解
- 资源易于获取和准备
- 时间分配现实可行
- 提供备用方案

### 4. 创新性
- 活动设计有趣生动
- 技术手段合理运用
- 鼓励个性化调整

## 质量保证

### 守门条件
- **Orchestrator**：材料审核完成，至少有教材或课程标准 ⭐新增
- **Curriculum Analyst**：基于材料完成分析，教学目标明确，重难点清晰
- **Content Designer**：内容准确，呈现方式科学
- **Activity Designer**：活动有效，时间合理
- **Resource Coordinator**：资源完整，来源明确
- **Assessment Expert**：评估多元，与目标对齐
- **Quality Reviewer**：全面审核，签字确认

### 审核维度
1. **教学目标**：明确性、可测量性、可达成性
2. **内容设计**：准确性、地道性、适切性
3. **活动设计**：有效性、可行性、趣味性
4. **资源准备**：完整性、可获取性、版权合规
5. **评估设计**：多样性、对齐性、可操作性
6. **完整性**：文档齐全、逻辑清晰、衔接流畅

## 技术架构

### 状态管理
- 基于文件系统的状态持久化
- YAML 格式的状态机定义
- Markdown 格式的文档管理

### 代理协作
- 依赖关系明确，避免循环依赖
- 交接验证机制，确保质量
- 返工流程，支持迭代改进

### 资源管理
- 用户材料管理（`materials/`）⭐新增
- 集中式资源存储（`assets/`）
- 统一的来源记录（`state/SOURCES.md`）
- 版权信息跟踪

## 扩展性

系统设计支持：
- 添加新的代理角色
- 修改工作流程
- 自定义审核标准
- 集成外部工具和服务

## 与 Claude Skills 的集成

- **标准接口**：通过命令行调用
- **状态持久化**：支持多会话和断点续传
- **权限管理**：细粒度的访问控制
- **组合能力**：可与其他 Skills 协同工作

详细规范请参考 `CLAUDE.md`。
