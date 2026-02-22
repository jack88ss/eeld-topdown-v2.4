# ⏱️ Sisyphus 自动决策机制

## 🎯 核心原则

**超过 1 分钟用户未确认时，由 Sisyphus 自行决策是否进入下一环节，或补充内容后继续。**

---

## 📋 工作流程

### 阶段 4：Big Task Proposal（核心大任务建议）

```
┌─────────────────────────────────────────────┐
│ 1. Sisyphus 生成核心大任务建议              │
│    - 提出 1-3 个创新大任务方案              │
│    - 生成 state/BIG_TASK_PROPOSAL.md        │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ 2. 等待用户确认（最多 60 秒）               │
│    ⏰ 倒计时开始...                         │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌─────────────┐    ┌─────────────────┐
│ 用户确认    │    │ 60秒超时        │
│ (正常流程)  │    │ (自动决策)      │
└─────────────┘    └────────┬────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │ 3. Sisyphus 自动评估提案质量      │
        │                                   │
        │ 评估维度：                        │
        │ ✓ 教学目标对齐度 (30%)            │
        │ ✓ 学生能力匹配度 (30%)            │
        │ ✓ 任务可行性 (25%)                │
        │ ✓ 创新性与趣味性 (15%)            │
        │                                   │
        │ 计算综合得分 (0-100)              │
        └───────────────┬───────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐           ┌─────────────────┐
│ 得分 ≥ 90       │           │ 得分 80-89      │
│ (优秀)          │           │ (良好)          │
│                 │           │                 │
│ 决策：          │           │ 决策：          │
│ ✅ 直接进入     │           │ 🔧 微调后进入   │
│   下一阶段      │           │   下一阶段      │
│                 │           │                 │
│ 理由：          │           │ 调整项：        │
│ 提案质量优秀    │           │ - 优化任务描述  │
│ 无需修改        │           │ - 调整难度      │
│                 │           │ - 补充支架      │
└─────────────────┘           └─────────────────┘
        │                               │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ 得分 < 80                     │
        │ (需改进)                      │
        │                               │
        │ 决策：                        │
        │ 📝 补充备选方案后进入下一阶段 │
        │                               │
        │ 补充内容：                    │
        │ - 提供 2-3 个备选大任务       │
        │ - 分析各方案优缺点            │
        │ - 标注推荐方案                │
        │ - 保留原方案作为参考          │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ 4. 记录决策日志               │
        │    state/DECISION_LOG.md      │
        │                               │
        │ - 决策时间                    │
        │ - 评估得分                    │
        │ - 决策理由                    │
        │ - 调整内容                    │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ 5. 自动进入阶段 5             │
        │    Activity Design            │
        └───────────────────────────────┘
```

---

## 📊 评估标准详解

### 1. 教学目标对齐度 (30%)

评估大任务是否能有效达成课程标准和单元目标。

**评分标准**：
- **90-100分**：完全对齐核心目标，覆盖所有语言点和能力目标
- **80-89分**：基本对齐，个别目标覆盖不够充分
- **70-79分**：部分对齐，需要补充或调整任务设计
- **<70分**：偏离目标，需要重新设计

**示例**：
```
Unit 1 目标：能够用 There is/are 描述房间和物品
优秀大任务：设计梦想房间并介绍（直接应用语法）
一般大任务：学习家具词汇（未体现语法应用）
```

### 2. 学生能力匹配度 (30%)

评估任务难度是否适合五年级学生的认知和语言水平。

**评分标准**：
- **90-100分**：难度适中，挑战性与支架性平衡
- **80-89分**：略偏难/易，但可通过调整支架解决
- **70-79分**：难度不当，需要重新设计或分解任务
- **<70分**：完全不适合，需要重新构思

**Goldilocks 原则**：
- Not too hard（不会让学生挫败）
- Not too easy（不会让学生无聊）
- Just right（恰到好处的挑战）

### 3. 任务可行性 (25%)

评估任务在实际课堂中的可操作性。

**考虑因素**：
- ✓ 时间：一节课（40分钟）能否完成
- ✓ 资源：所需材料是否容易获取
- ✓ 组织：课堂管理是否可控
- ✓ 评估：学习成果是否可观察和评价

**评分标准**：
- **90-100分**：完全可行，资源充足，易于实施
- **80-89分**：基本可行，需要少量调整或准备
- **70-79分**：可行性一般，需要较多准备或调整
- **<70分**：难以实施，需要重新设计

### 4. 创新性与趣味性 (15%)

评估任务是否能激发学生兴趣和参与度。

**评分标准**：
- **90-100分**：创意新颖，与学生生活紧密相关，趣味性强
- **80-89分**：有一定创意，学生会感兴趣
- **70-79分**：常规任务，趣味性一般
- **<70分**：枯燥乏味，难以激发兴趣

---

## 🤖 Sisyphus 决策逻辑

### 决策 1：直接进入下一阶段 (得分 ≥ 90)

```javascript
if (evaluationScore >= 90) {
  decision = "PROCEED_DIRECTLY";
  reason = "提案质量优秀，无需修改";
  logDecision({
    stage: "big_task_proposal",
    score: evaluationScore,
    decision: decision,
    reason: reason,
    timestamp: now()
  });
  moveToNextStage("activity_design");
}
```

**记录示例**：
```markdown
## 决策记录 - 2026-01-20 12:30:00

**阶段**：Big Task Proposal
**评估得分**：95/100
**决策**：直接进入下一阶段

**评估详情**：
- 教学目标对齐度：30/30 ✓
- 学生能力匹配度：29/30 ✓
- 任务可行性：23/25 ✓
- 创新性与趣味性：13/15 ✓

**决策理由**：
提案质量优秀，核心大任务"续写 Goldilocks 故事并角色扮演"完全符合教学目标，
难度适中，可行性强，且具有高度趣味性。无需用户确认，直接进入活动设计阶段。
```

---

### 决策 2：微调后进入 (得分 80-89)

```javascript
if (evaluationScore >= 80 && evaluationScore < 90) {
  decision = "ADJUST_AND_PROCEED";
  adjustments = identifyAdjustments(proposal, weakPoints);
  adjustedProposal = applyAdjustments(proposal, adjustments);
  
  logDecision({
    stage: "big_task_proposal",
    score: evaluationScore,
    decision: decision,
    adjustments: adjustments,
    timestamp: now()
  });
  
  updateProposal(adjustedProposal);
  moveToNextStage("activity_design");
}
```

**调整示例**：

**原提案**（得分 85）：
```
核心大任务：续写 Goldilocks 故事
学生分组续写故事结尾，然后全班分享。
```

**问题识别**：
- ✓ 目标对齐：28/30（缺少语法明确应用）
- ✓ 能力匹配：27/30（语言支架不足）
- ✓ 可行性：20/25（时间分配不明确）
- ✓ 创新性：10/15（常规写作任务）

**Sisyphus 自动调整**：
```markdown
## 微调后的提案

### 核心大任务：续写 Goldilocks 故事并创作新场景

**任务描述**：
学生分组创作 Goldilocks 进入 bears' house 后的新场景，
使用 "There is/are..." 描述房间和物品。

**语言支架**：
- 提供场景词汇库（kitchen, bathroom, bedroom, garden）
- 提供句型框架：
  - In the [room], there is a [object].
  - There are [number] [objects] on/in/under the [furniture].

**时间分配**：
- 小组讨论和创作：15分钟
- 小组展示：10分钟
- 全班投票最佳创意：3分钟

**调整说明**：
1. 明确语法应用要求（There is/are）
2. 提供语言支架降低难度
3. 明确时间分配提高可行性
4. 增加投票环节提升趣味性

**调整后得分预估**：92/100
```

---

### 决策 3：补充备选方案 (得分 < 80)

```javascript
if (evaluationScore < 80) {
  decision = "SUPPLEMENT_ALTERNATIVES";
  alternatives = generateAlternatives(proposal, evaluationFeedback);
  
  supplementedProposal = {
    original: proposal,
    evaluation: evaluationFeedback,
    alternatives: alternatives,
    recommendation: selectBestAlternative(alternatives)
  };
  
  logDecision({
    stage: "big_task_proposal",
    score: evaluationScore,
    decision: decision,
    alternatives: alternatives.map(a => a.title),
    timestamp: now()
  });
  
  updateProposal(supplementedProposal);
  moveToNextStage("activity_design");
}
```

**补充示例**：

**原提案**（得分 72）：
```
核心大任务：背诵 Goldilocks 故事
学生熟读故事，然后背诵关键段落。
```

**问题识别**：
- ✗ 目标对齐：18/30（只关注记忆，未体现语言应用）
- ✓ 能力匹配：24/30（难度适中但意义不大）
- ✓ 可行性：20/25（可以实施）
- ✗ 创新性：10/15（传统机械记忆）

**Sisyphus 补充方案**：

```markdown
## 原方案保留（不推荐）

**核心大任务：背诵 Goldilocks 故事**
- 得分：72/100
- 问题：只关注记忆，未体现语言应用和创新性
- 建议：仅作为预热活动，不作为核心大任务

---

## 备选方案 A：家居设计师（推荐 ⭐⭐⭐）

**任务描述**：
学生扮演家居设计师，为 Three Bears 设计新家。
小组合作绘制房间平面图，用 There is/are 描述家具摆放。

**语言应用**：
- There is a big bed in Papa Bear's bedroom.
- There are three chairs in the dining room.
- There is a computer on the desk.

**评估预估**：
- 目标对齐：29/30 ✓（直接应用语法）
- 能力匹配：28/30 ✓（创意 + 语言）
- 可行性：24/25 ✓（纸笔即可）
- 创新性：14/15 ✓（贴近生活）
- **总分：95/100**

---

## 备选方案 B：故事改编剧场

**任务描述**：
小组改编 Goldilocks 故事，创造不同结局。
设计新场景（如 bears 回家后的对话），使用目标语言演绎。

**语言应用**：
- Goldilocks: "I'm sorry! There was no one at home."
- Baby Bear: "Look! There are broken chairs everywhere!"
- Mama Bear: "There is someone sleeping in my bed!"

**评估预估**：
- 目标对齐：27/30 ✓
- 能力匹配：26/30 ✓
- 可行性：22/25 ✓
- 创新性：13/15 ✓
- **总分：88/100**

---

## 备选方案 C：房间寻宝游戏

**任务描述**：
教师布置虚拟"Bears' House"线索，学生用 There is/are 提问寻找宝藏。

**语言应用**：
- Student A: "Is there a key under the chair?"
- Student B: "No, there isn't. But there are three keys in the kitchen."

**评估预估**：
- 目标对齐：28/30 ✓
- 能力匹配：27/30 ✓
- 可行性：20/25 ✓（需要教师准备）
- 创新性：14/15 ✓
- **总分：89/100**

---

## Sisyphus 推荐

**推荐方案**：备选方案 A - 家居设计师 ⭐⭐⭐

**推荐理由**：
1. ✅ 直接应用核心语法 There is/are
2. ✅ 难度适中，五年级学生可驾驭
3. ✅ 资源需求低（纸笔即可）
4. ✅ 贴近学生生活，趣味性强
5. ✅ 成果可视化，便于展示和评价

**实施建议**：
- Pre-task: 复习家具词汇和 There is/are 句型
- While-task: 小组设计并描述房间
- Post-task: Gallery Walk 欣赏各组作品

**决策**：采用备选方案 A，进入活动设计阶段
```

---

## 📝 决策日志记录

每次自动决策都会记录到 `state/DECISION_LOG.md`：

```markdown
# Sisyphus 自动决策日志

## 2026-01-20 Session

### Decision #1 - 12:30:15

**Stage**: Big Task Proposal (阶段 4)
**Trigger**: User confirmation timeout (60 seconds)
**Evaluation Score**: 85/100

**Breakdown**:
- 教学目标对齐度: 28/30
- 学生能力匹配度: 27/30
- 任务可行性: 20/25
- 创新性与趣味性: 10/15

**Decision**: ADJUST_AND_PROCEED (微调后进入下一阶段)

**Adjustments Made**:
1. 添加明确的语法应用要求
2. 提供语言支架（词汇库和句型框架）
3. 明确时间分配（15min + 10min + 3min）
4. 增加投票环节提升趣味性

**Adjusted Score (Estimated)**: 92/100

**Next Stage**: Activity Design (阶段 5)
**Timestamp**: 2026-01-20T12:30:15+08:00

---
```

---

## ⚙️ 配置文件位置

自动决策机制的配置在：

**`.opencode/oh-my-opencode.config.json`**

```json
{
  "agents": {
    "sisyphus": {
      "autonomy": {
        "enabled": true,
        "level": "high",
        "decision_making": {
          "user_timeout_threshold_seconds": 60,
          "auto_evaluation_enabled": true,
          "quality_threshold": 80,
          "fallback_strategy": "supplement_and_proceed"
        }
      }
    }
  },
  "workflows": {
    "lesson_design": {
      "auto_proceed_on_timeout": true,
      "user_confirmation_timeout_seconds": 60,
      "stages": [
        {
          "id": "big_task_proposal",
          "requires_user_confirmation": true,
          "confirmation_timeout_seconds": 60,
          "on_timeout": {
            "action": "auto_proceed_with_review"
          }
        }
      ]
    }
  }
}
```

---

## 🎯 使用场景

### 场景 1：教师离开电脑

```
12:00 - Sisyphus 生成大任务建议，等待确认
12:01 - 教师临时离开（接电话/处理学生问题）
12:01 - ⏰ 倒计时开始...
        60秒...50秒...40秒...
12:02 - ⏰ 超时！
        Sisyphus 自动评估：得分 92/100
        决策：直接进入下一阶段
12:03 - 教师回来，发现工作流已自动继续
        查看 DECISION_LOG.md 了解决策理由
```

### 场景 2：批量生成模式

```
用户需求："今晚帮我准备 5 个单元的教案"

传统模式：
- 每个单元阶段 4 都需要确认
- 5 个单元 = 5 次打断
- 无法无人值守运行

自动模式：
- 启动任务后可以离开
- Sisyphus 自动评估和决策
- 早上起来 5 个教案全部完成 ✓
```

### 场景 3：信任 AI 的教师

```
"我信任 Sisyphus 的专业判断，
不需要每次都确认，
除非有严重问题才通知我。"

配置：
{
  "user_confirmation_timeout_seconds": 10,
  "alert_only_on_low_score": true,
  "low_score_threshold": 70
}
```

---

## 🔔 告警机制

### 何时通知用户

即使自动决策，以下情况仍会告警：

1. **评估得分 < 70**
   - 提案质量较差
   - 虽然已补充备选方案，但建议用户关注

2. **预算超限**
   - API 调用成本超过每日限额 80%
   - 建议切换到更便宜的模型

3. **错误发生**
   - API 调用失败
   - 文件生成错误
   - 模型响应异常

### 告警方式

- 📧 在 OpenCode 界面显示通知
- 📝 记录到 `state/ALERTS.log`
- 🔊 （可选）系统通知音

---

## 🎉 总结

### ✅ 优势

1. **无需值守**：启动后可以离开，Sisyphus 自动完成
2. **智能决策**：基于多维度评估，不是简单通过
3. **质量保证**：低分方案会补充备选，确保教学质量
4. **全程记录**：所有决策可追溯，透明可信
5. **灵活可调**：超时时间、评分阈值均可自定义

### 📊 预期效果

- ⏱️ **节省时间**：教师无需实时确认，工作流自动运行
- 🤖 **AI 赋能**：充分发挥 Sisyphus 的专业能力
- 📈 **批量生成**：可以一次性生成多个单元教案
- 🎯 **质量可靠**：自动评估机制确保输出质量

---

**现在，你可以真正实现"睡一觉，教案就好了"！** 🌙✨
