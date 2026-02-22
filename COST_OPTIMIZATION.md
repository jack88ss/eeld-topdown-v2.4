# 💰 成本优化策略

## 📊 模型定价对比（每百万 tokens）

| 模型 | 输入成本 | 输出成本 | 上下文 | 适用场景 |
|------|---------|---------|--------|---------|
| **Gemini Pro 1.5** | $0.125 | $0.375 | 1M | 📚 大文件处理 |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 | 200K | 🧠 深度推理 |
| **Claude 3 Haiku** | $0.25 | $1.25 | 200K | ⚡ 快速任务 |
| **GPT-4o** | $2.50 | $10.00 | 128K | 💻 代码生成 |

---

## 🎯 9 个阶段的模型分配策略

### ✅ **高价值任务（使用 Claude 3.5 Sonnet）**

**阶段 1: Material Intake** → **Gemini Pro 1.5**
- 💰 成本：**低** （大文件但便宜）
- 📚 原因：1M 上下文，读取整本教材 PDF
- 💡 优化：一次性读完，避免多次调用

**阶段 2: Curriculum Analysis** → **Claude 3.5 Sonnet**
- 💰 成本：**高** （但必要）
- 🧠 原因：需要专业教学分析和判断
- 💡 优化：一次性完成完整分析

**阶段 3: Content Design** → **Claude 3.5 Sonnet**
- 💰 成本：**高** （但必要）
- 🎨 原因：核心教学设计，质量优先
- 💡 优化：一次性设计完整流程

**阶段 4: Big Task Proposal** → **Claude 3.5 Sonnet**
- 💰 成本：**高** （但必要）
- 💡 原因：关键决策点，需要专业判断
- 💡 优化：暂停等待用户确认，避免重复生成

---

### ⚡ **中低价值任务（使用 Claude 3 Haiku）**

**阶段 5: Activity Design** → **Claude 3 Haiku**
- 💰 成本：**低** （Haiku 便宜 12 倍）
- ⚡ 原因：基于已确定的大任务，细化具体活动
- 💡 优化：已有明确框架，Haiku 足够

**阶段 6: Resource Coordination** → **Claude 3 Haiku**
- 💰 成本：**低**
- 📋 原因：简单整理和清单工作
- 💡 优化：无需高级推理能力

**阶段 7: Assessment Design** → **Claude 3.5 Sonnet**
- 💰 成本：**高** （但必要）
- 📊 原因：评估设计需要专业能力
- 💡 优化：确保评估质量

**阶段 8: Quality Review** → **Claude 3 Haiku**
- 💰 成本：**低**
- ✅ 原因：检查一致性和格式问题
- 💡 优化：基于规则检查，Haiku 足够

**阶段 9: Package Publish** → **Claude 3 Haiku**
- 💰 成本：**低**
- 📦 原因：格式化和整合工作
- 💡 优化：模板化输出，无需高级推理

---

## 📈 成本预估（单次完整流程）

### 保守估计（200K tokens 输入 + 50K tokens 输出）

| 阶段 | 模型 | 输入 tokens | 输出 tokens | 输入成本 | 输出成本 | 小计 |
|------|------|-----------|-----------|---------|---------|------|
| 1. Material Intake | Gemini Pro 1.5 | 500K | 10K | $0.063 | $0.004 | **$0.067** |
| 2. Curriculum Analysis | Claude 3.5 Sonnet | 150K | 15K | $0.450 | $0.225 | **$0.675** |
| 3. Content Design | Claude 3.5 Sonnet | 150K | 20K | $0.450 | $0.300 | **$0.750** |
| 4. Big Task Proposal | Claude 3.5 Sonnet | 100K | 10K | $0.300 | $0.150 | **$0.450** |
| 5. Activity Design | Claude 3 Haiku | 100K | 15K | $0.025 | $0.019 | **$0.044** |
| 6. Resource Coordination | Claude 3 Haiku | 50K | 10K | $0.013 | $0.013 | **$0.026** |
| 7. Assessment Design | Claude 3.5 Sonnet | 100K | 15K | $0.300 | $0.225 | **$0.525** |
| 8. Quality Review | Claude 3 Haiku | 150K | 10K | $0.038 | $0.013 | **$0.051** |
| 9. Package Publish | Claude 3 Haiku | 50K | 20K | $0.013 | $0.025 | **$0.038** |

**总计：约 $2.63 / 课**

---

## 🚀 成本优化措施

### 1. **智能模型路由**
```javascript
// Oh My OpenCode 自动根据任务类型选择模型
if (task.requires_reasoning) {
  model = "claude-3.5-sonnet";  // 高质量推理
} else if (task.involves_large_files) {
  model = "gemini-pro-1.5";     // 长上下文
} else {
  model = "claude-3-haiku";     // 快速便宜
}
```

### 2. **上下文压缩**
- ✅ 阶段 5-9 只传递必要的前序结果
- ✅ 不传递原始教材 PDF（仅传递提取的关键信息）
- ✅ 使用 Markdown 摘要代替完整文档

### 3. **批处理和缓存**
- ✅ 阶段 1 一次性读取所有材料
- ✅ 阶段 4 暂停确认，避免后续重做
- ✅ 缓存 API 响应（OpenRouter 支持）

### 4. **预算控制**
```json
{
  "budget": {
    "daily_limit_usd": 5.0,
    "alert_threshold": 0.8,
    "auto_switch_to_haiku": true
  }
}
```

### 5. **降级策略**
- 🚨 如果超预算 → 自动切换到 Claude 3 Haiku
- 🚨 如果 API 失败 → 降级到更便宜的模型
- 🚨 如果上下文过长 → 切换到 Gemini Pro 1.5

---

## 💡 最佳实践

### ✅ **省钱技巧**

1. **使用 Haiku 处理简单任务**
   - 资源整理、格式化、清单生成
   - 节省 **12 倍成本**

2. **Gemini Pro 1.5 处理大文件**
   - 阅读教材 PDF、课程标准
   - 比 Claude 3.5 Sonnet 便宜 **24 倍**

3. **只在关键阶段使用 Sonnet**
   - 课程分析、内容设计、评估设计
   - 确保教学质量

4. **避免重复生成**
   - 阶段 4 暂停确认，一次成功
   - 减少重试次数

5. **监控实时成本**
   - Oh My OpenCode 自动记录每次调用成本
   - 查看 `state/LOG.md` 的成本统计

---

## 📊 成本对比：优化前 vs 优化后

| 方案 | 模型策略 | 单课成本 | 10 课成本 |
|------|---------|---------|----------|
| **优化前** | 全部 Claude 3.5 Sonnet | ~$4.50 | ~$45.00 |
| **优化后** | 智能混合使用 | ~$2.63 | ~$26.30 |
| **节省** | - | **41%** | **$18.70** |

---

## 🎯 使用建议

### 推荐配置（平衡质量与成本）

```json
{
  "stage_1_material_intake": "gemini-pro-1.5",      // 大文件便宜
  "stage_2_curriculum_analysis": "claude-3.5-sonnet", // 质量优先
  "stage_3_content_design": "claude-3.5-sonnet",     // 质量优先
  "stage_4_big_task_proposal": "claude-3.5-sonnet",  // 关键决策
  "stage_5_activity_design": "claude-3-haiku",       // 节省成本
  "stage_6_resource_coordination": "claude-3-haiku", // 节省成本
  "stage_7_assessment_design": "claude-3.5-sonnet",  // 质量优先
  "stage_8_quality_review": "claude-3-haiku",        // 节省成本
  "stage_9_package_publish": "claude-3-haiku"        // 节省成本
}
```

### 预算有限（最低成本）

全部使用 **Claude 3 Haiku** + **Gemini Pro 1.5**（仅阶段 1）
- 单课成本：**~$0.35**
- 质量：中等（适合草稿和练习）

### 质量优先（不考虑成本）

全部使用 **Claude 3.5 Sonnet**
- 单课成本：**~$4.50**
- 质量：最高（适合公开课和精品课）

---

## 🔍 成本监控

### 查看实时成本

```bash
# 查看总成本
cat state/LOG.md | grep "Cost:"

# 查看各阶段成本
cat state/LOG.md | grep "Stage.*Cost"

# 查看今日成本
cat state/LOG.md | grep "$(date +%Y-%m-%d)" | grep "Cost"
```

### 成本告警

Oh My OpenCode 会在以下情况自动告警：

- 🚨 单次调用超过 $1.00
- 🚨 单课总成本超过 $5.00
- 🚨 今日累计超过预算 80%

---

## 📌 总结

✅ **最优策略**：智能混合使用多个模型
✅ **关键原则**：高价值任务用好模型，简单任务用便宜模型
✅ **成本节省**：相比全部使用 Sonnet，节省 **41% 成本**
✅ **质量保证**：核心阶段仍使用最强模型，确保教学质量

**单课成本控制在 $2.63，质量与成本的最佳平衡！** 🎉
