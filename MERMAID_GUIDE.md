# Mermaid图表使用指南

## 概述
Mermaid是一种基于文本的图表生成工具，可以直接在Markdown中创建各种图表，无需外部工具或图片文件。

## 适用场景与图表类型

### 1. 流程图（Flowchart）
用于展示步骤、决策流程、工作流

```mermaid
graph TD
    A[用户输入] --> B{是否有图片?}
    B -->|是| C[智能放置图片]
    B -->|否| D{概念复杂?}
    D -->|是| E[生成Mermaid图]
    D -->|否| F[纯文字描述]
```

### 2. 时序图（Sequence Diagram）
用于展示交互过程、API调用、代理协作

```mermaid
sequenceDiagram
    participant U as 用户
    participant S as Stylist
    participant W as Writer
    participant E as Editor

    U->>S: 提供写作主题
    S->>S: 分析风格
    S->>W: 传递风格要求
    W->>W: 创作内容
    W->>E: 提交草稿
    E->>U: 交付成品
```

### 3. 甘特图（Gantt Chart）
用于展示项目进度、时间安排

```mermaid
gantt
    title 博客写作流程时间线
    dateFormat  YYYY-MM-DD
    section 准备阶段
    风格分析           :a1, 2024-01-01, 1d
    素材收集           :a2, after a1, 2d
    section 创作阶段
    大纲设计           :b1, after a2, 1d
    内容撰写           :b2, after b1, 3d
    section 完善阶段
    编辑审核           :c1, after b2, 1d
    发布准备           :c2, after c1, 1d
```

### 4. 饼图（Pie Chart）
用于展示比例、分布、构成

```mermaid
pie title 文章内容构成
    "技术介绍" : 30
    "案例分析" : 35
    "实践指南" : 25
    "总结展望" : 10
```

### 5. 类图（Class Diagram）
用于展示系统架构、模块关系

```mermaid
classDiagram
    class BlogSystem {
        +String topic
        +String style
        +generateContent()
    }
    class Agent {
        <<interface>>
        +execute()
        +log()
    }
    class Writer {
        +draft()
        +revise()
    }
    class Editor {
        +review()
        +approve()
    }

    BlogSystem --> Agent
    Writer ..|> Agent
    Editor ..|> Agent
```

### 6. 状态图（State Diagram）
用于展示状态转换、生命周期

```mermaid
stateDiagram-v2
    [*] --> 计划
    计划 --> 调研
    调研 --> 撰写
    撰写 --> 审核
    审核 --> 发布: 通过
    审核 --> 撰写: 需修改
    发布 --> [*]
```

## 使用原则

### 何时使用Mermaid
1. **流程说明**：多步骤的操作流程
2. **架构展示**：系统组件关系
3. **数据对比**：比例、分布数据
4. **时间顺序**：事件发展、交互过程
5. **状态变化**：状态机、生命周期

### 何时不使用
1. **简单概念**：一两句话能说清楚的
2. **纯数据**：适合表格展示的
3. **UI界面**：需要截图的
4. **艺术配图**：需要美观装饰的

## 在博客中的应用示例

### 技术流程图
```markdown
下面是规格驱动开发的四个阶段：

```mermaid
graph LR
    A[Specify<br/>明确需求] --> B[Plan<br/>制定计划]
    B --> C[Tasks<br/>拆解任务]
    C --> D[Implementation<br/>具体实现]

    style A fill:#e1f5fe
    style B fill:#fff9c4
    style C fill:#f3e5f5
    style D fill:#e8f5e9
```

### 性能对比图
```markdown
不同AI工具的效率对比：

```mermaid
graph TB
    subgraph "耗时对比"
        A[Claude Code: 1h17m]
        B[Gemini CLI: 2h02m]
        C[传统方式: 3h+]
    end
    subgraph "成本对比"
        D[Claude: $4.80]
        E[Gemini: $7.06]
        F[传统: $10+]
    end
```

### 决策流程
```markdown
选择开发方式的决策树：

```mermaid
graph TD
    A[项目规模] -->|小型| B[直接编码]
    A -->|中型| C[简单规格]
    A -->|大型| D[完整规格驱动]

    C --> E{团队规模}
    E -->|个人| F[轻量规格]
    E -->|团队| G[标准规格]

    D --> H[必须规格驱动]
```

## 最佳实践

1. **保持简洁**：图表应该辅助理解，不要过于复杂
2. **统一风格**：全文图表风格保持一致
3. **适度使用**：每篇文章2-4个图表为宜
4. **配合文字**：图表前后要有说明文字
5. **响应式考虑**：确保移动端也能正常显示

## 代理使用指导

### Writer代理
- 识别复杂概念，主动使用Mermaid图表
- 每个图表前后加说明文字
- 图表复杂度适中（5-10个节点）

### Editor代理
- 检查图表是否有助于理解
- 确认图表语法正确
- 评估是否需要简化或拆分

### Publisher代理
- 验证Mermaid代码块正确渲染
- 确保发布平台支持Mermaid
- 必要时提供PNG备选方案

## 常见错误与解决

1. **语法错误**：使用在线编辑器预览
2. **过于复杂**：拆分成多个小图
3. **文字过长**：使用缩写或分行
4. **样式不一致**：定义统一的样式模板
5. **渲染失败**：检查特殊字符转义
