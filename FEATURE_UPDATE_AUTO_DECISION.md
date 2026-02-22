# 🎉 新功能：Sisyphus 自动决策机制

**更新日期**：2026-01-20  
**版本**：v2.5.0

---

## 🆕 新增功能

### ⏱️ 超时自动决策

**功能描述**：
当用户在阶段 4（Big Task Proposal）需要确认时，如果 **60 秒内没有响应**，Sisyphus 将：
1. 自动评估提案质量（0-100 分）
2. 根据评分智能决策下一步行动
3. 记录决策日志供后续查看

**解决的问题**：
- ❌ 用户临时离开，工作流被迫暂停
- ❌ 无法实现批量无人值守生成
- ❌ 每个单元都需要实时确认，效率低

**现在可以**：
- ✅ 启动任务后可以离开
- ✅ 批量生成多个单元教案
- ✅ "睡一觉，教案就好了"

---

## 🎯 决策逻辑

### 评估维度（4 个方面，总分 100）

| 维度 | 权重 | 评估内容 |
|------|------|---------|
| **教学目标对齐度** | 30% | 大任务是否能达成课程标准和单元目标 |
| **学生能力匹配度** | 30% | 任务难度是否适合五年级学生水平 |
| **任务可行性** | 25% | 课堂实施是否可行（时间、资源、组织） |
| **创新性与趣味性** | 15% | 是否能激发学生兴趣和参与度 |

### 决策规则

```
┌─────────────┬──────────────────┬────────────────────────────┐
│ 评估得分    │ Sisyphus 决策    │ 具体行动                   │
├─────────────┼──────────────────┼────────────────────────────┤
│ ≥ 90 分     │ ✅ 直接继续      │ 提案优秀，无需修改         │
│ 80-89 分    │ 🔧 微调后继续    │ 优化描述、调整难度、补充支架│
│ < 80 分     │ 📝 补充备选方案  │ 提供 2-3 个替代方案 + 推荐  │
└─────────────┴──────────────────┴────────────────────────────┘
```

---

## 📊 工作流程对比

### 优化前（传统模式）

```
┌──────────────────────────┐
│ Stage 4: 生成大任务建议   │
└─────────────┬────────────┘
              │
              ▼
      ⏸️ 暂停等待用户确认
              │
              ▼ (用户必须在场)
      ✅ 用户确认或修改
              │
              ▼
┌──────────────────────────┐
│ Stage 5: 继续活动设计     │
└──────────────────────────┘

❌ 问题：
- 用户离开 = 工作流暂停
- 批量生成 = 需要多次确认
- 无法无人值守运行
```

### 优化后（自动决策模式）

```
┌──────────────────────────┐
│ Stage 4: 生成大任务建议   │
└─────────────┬────────────┘
              │
              ▼
      ⏰ 等待确认（60秒）
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
   用户确认      超时无响应
       │             │
       │             ▼
       │      🤖 Sisyphus 自动评估
       │             │
       │        ┌────┴────┐
       │        │         │
       │        ▼         ▼
       │     得分≥90   得分<90
       │        │         │
       │        │         ▼
       │        │    微调/补充方案
       │        │         │
       └────────┴─────────┘
                │
                ▼
┌──────────────────────────┐
│ Stage 5: 继续活动设计     │
└──────────────────────────┘

✅ 优势：
- 用户可以离开，工作流自动继续
- 批量生成无需多次确认
- 支持无人值守运行
```

---

## 📝 决策记录示例

每次自动决策都会记录到 `state/DECISION_LOG.md`：

```markdown
# Sisyphus 自动决策日志

## 2026-01-20 Session

### Decision #1 - 12:30:15

**Stage**: Big Task Proposal (阶段 4)
**Trigger**: User confirmation timeout (60 seconds)
**Evaluation Score**: 92/100

**Breakdown**:
- 教学目标对齐度: 29/30 ✓
- 学生能力匹配度: 28/30 ✓
- 任务可行性: 23/25 ✓
- 创新性与趣味性: 12/15 ✓

**Decision**: PROCEED_DIRECTLY

**Reason**: 
提案质量优秀。核心大任务"家居设计师 - 为 Three Bears 设计新家"
完全符合教学目标（直接应用 There is/are 语法），难度适中，
可行性强，且具有高度趣味性。无需修改，直接进入活动设计阶段。

**Next Stage**: Activity Design (阶段 5)
**Timestamp**: 2026-01-20T12:30:15+08:00
```

---

## 🔧 配置文件

### `.opencode/oh-my-opencode.config.json`

新增配置项：

```json
{
  "agents": {
    "sisyphus": {
      "model": "openrouter/anthropic/claude-3.5-sonnet",
      "temperature": 0.7,
      "autonomy": {
        "enabled": true,                    // ← 启用自主决策
        "level": "high",                    // ← 高度自主
        "decision_making": {
          "user_timeout_threshold_seconds": 60,  // ← 超时时间
          "auto_evaluation_enabled": true,       // ← 启用自动评估
          "quality_threshold": 80,               // ← 质量阈值
          "fallback_strategy": "supplement_and_proceed"
        }
      }
    }
  },
  "workflows": {
    "lesson_design": {
      "auto_proceed_on_timeout": true,           // ← 超时自动继续
      "user_confirmation_timeout_seconds": 60,   // ← 确认超时时间
      "stages": [
        {
          "id": "big_task_proposal",
          "requires_user_confirmation": true,
          "confirmation_timeout_seconds": 60,    // ← 阶段超时
          "on_timeout": {
            "action": "auto_proceed_with_review" // ← 超时行为
          }
        }
      ]
    }
  }
}
```

---

## 💡 使用场景

### 场景 1：批量生成（推荐 ⭐⭐⭐）

**需求**：
```
今晚需要准备 5 个单元的教案
```

**操作**：
```bash
# 1. 启动 OpenCode
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down
opencode

# 2. 输入任务（可以去睡觉了）
ulw Design lessons for Units 1-5, Grade 5, Yilin Press

# 3. 早上起来查看结果
draft/unit1_lesson_plan.md
draft/unit2_lesson_plan.md
draft/unit3_lesson_plan.md
draft/unit4_lesson_plan.md
draft/unit5_lesson_plan.md
```

**预期成本**：
- 5 个单元 × $2.63/单元 = **约 $13.15**
- 时间：自动运行，无需值守

---

### 场景 2：临时离开

**需求**：
```
正在生成教案，但需要临时处理其他事情
```

**操作**：
```
1. 启动任务后直接离开
2. Sisyphus 在阶段 4 等待 60 秒
3. 超时后自动评估和决策
4. 回来后查看 state/DECISION_LOG.md 了解决策理由
```

---

### 场景 3：信任 AI（高级用户）

**需求**：
```
我信任 Sisyphus 的专业判断，不需要每次都确认
```

**配置**：
```json
{
  "user_confirmation_timeout_seconds": 10,  // 改为 10 秒
  "auto_evaluation_enabled": true,
  "alert_only_on_low_score": true,          // 只在低分时告警
  "low_score_threshold": 70
}
```

**效果**：
- 等待时间缩短到 10 秒
- 只有质量较差（<70 分）时才通知
- 其他情况全自动运行

---

## 🔔 告警机制

即使自动决策，以下情况仍会告警：

| 情况 | 告警内容 | 建议 |
|------|---------|------|
| 评估得分 < 70 | 提案质量较差 | 查看补充的备选方案 |
| 预算超限 | API 成本超过 80% | 切换到更便宜的模型 |
| API 错误 | 调用失败或响应异常 | 检查网络和 API key |

---

## 📊 预期效果

### 时间节省

| 任务 | 传统模式 | 自动模式 | 节省 |
|------|---------|---------|------|
| 单个单元 | 40 分钟（含确认） | 35 分钟（无需等待） | 12.5% |
| 5 个单元 | 200 分钟（5×确认） | 175 分钟（无人值守） | 12.5% |
| 10 个单元 | 400 分钟（10×确认） | 350 分钟（睡一觉） | 12.5% |

### 用户体验

| 维度 | 传统模式 | 自动模式 |
|------|---------|---------|
| **便利性** | ⭐⭐ 需要实时在场 | ⭐⭐⭐⭐⭐ 无需值守 |
| **批量生成** | ⭐⭐ 多次打断 | ⭐⭐⭐⭐⭐ 一次启动 |
| **质量保证** | ⭐⭐⭐⭐⭐ 人工确认 | ⭐⭐⭐⭐ AI 评估 |
| **透明度** | ⭐⭐⭐ 实时查看 | ⭐⭐⭐⭐ 日志可追溯 |

---

## 📖 相关文档

1. **[AUTO_DECISION_MECHANISM.md](AUTO_DECISION_MECHANISM.md)**  
   完整的自动决策机制说明，包括评估标准、决策流程、示例等

2. **[QUICK_REFERENCE_AUTO_DECISION.md](QUICK_REFERENCE_AUTO_DECISION.md)**  
   快速参考卡片，便于日常使用

3. **[AGENTS.md](AGENTS.md)**  
   更新后的系统架构文档，包含自动决策部分

4. **[COST_OPTIMIZATION.md](COST_OPTIMIZATION.md)**  
   多模型成本优化策略

---

## 🎯 总结

### ✅ 核心价值

1. **无需值守**：启动后可以离开，Sisyphus 自动完成
2. **智能决策**：基于多维度评估，不是简单通过
3. **批量生成**：一次性生成多个单元教案
4. **质量保证**：低分方案会补充备选，确保教学质量
5. **全程记录**：所有决策可追溯，透明可信

### 🎉 一句话总结

**"超过 1 分钟用户未确认时，由 Sisyphus 自行决策进入下一环节或补充内容后继续。"**

现在，你可以真正实现 **"睡一觉，教案就好了"**！🌙✨

---

## 🚀 快速开始

```bash
# 1. 进入项目目录
cd C:\Users\Administrator\Desktop\myproject\eeld-top-down

# 2. 启动 OpenCode（或运行 .\.opencode\start-ohmyopencode.bat）
opencode

# 3. 输入任务（可以去忙别的了）
ulw Design lesson: Unit 1 Goldilocks, 五年级, 译林版

# 4. 等待完成（Sisyphus 会在 60 秒超时后自动决策）

# 5. 查看结果
- draft/lesson_plan.md          ← 完整教案
- state/DECISION_LOG.md         ← 决策记录
- state/BIG_TASK_PROPOSAL.md    ← 大任务方案
```

**开始你的无人值守教案生成之旅！** 🎉
