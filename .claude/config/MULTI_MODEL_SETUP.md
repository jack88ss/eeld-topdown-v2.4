# 多模型配置指南 - 解决大文件读取问题

> **解决方案**：使用 OpenRouter API 调用支持长上下文的便宜模型

---

## 🎯 问题描述

当前遇到的问题：
```
Read(materials\textbooks\译林版五上英语电子课本.pdf)
⎿ API Error: 413 {"error":{"type":"request_too_large","message":"Request exceeds the maximum size"}}
```

**原因**：PDF文件 24.1MB 超过了 Claude API 的请求大小限制。

**解决方案**：使用支持长上下文的模型，如 Google Gemini Pro 1.5（100万token上下文）。

---

## 🚀 快速开始

### 步骤 1：获取 OpenRouter API Key

1. 访问 https://openrouter.ai/
2. 注册账号
3. 创建 API Key
4. 复制 API Key

### 步骤 2：配置环境变量

**Windows (PowerShell)**:
```powershell
# 临时设置（当前会话有效）
$env:OPENROUTER_API_KEY = "sk-or-v1-your-key-here"

# 永久设置（推荐）
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-your-key-here', 'User')
```

**Linux/Mac (Bash)**:
```bash
# 临时设置
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 步骤 3：验证配置

```bash
# Windows PowerShell
echo $env:OPENROUTER_API_KEY

# Linux/Mac
echo $OPENROUTER_API_KEY
```

---

## 📋 模型选择策略

系统会根据任务类型自动选择合适的模型：

### 1. 长文本处理（读取教材、PDF）
**推荐模型**：`google/gemini-pro-1.5`
- **上下文窗口**：100万 tokens（约75万字）
- **成本**：$0.00125/1K input tokens，$0.005/1K output tokens
- **适用场景**：
  - ✅ 读取大型PDF教材（可达几十MB）
  - ✅ 分析完整课程标准文档
  - ✅ 处理教师教学用书

**示例成本计算**：
```
读取24MB PDF（约15万tokens）：
输入成本：150K × $0.00125/1K = $0.19
输出成本：2K × $0.005/1K = $0.01
总计：约 $0.20（不到2元人民币）
```

### 2. 教学设计和分析
**推荐模型**：`anthropic/claude-3.5-sonnet`
- **上下文窗口**：20万 tokens
- **成本**：$0.003/1K input tokens，$0.015/1K output tokens
- **适用场景**：
  - ✅ 课程分析
  - ✅ 内容设计
  - ✅ 活动设计
  - ✅ 核心大任务提议
  - ✅ 质量审核

### 3. 简单任务（资源整理）
**推荐模型**：`anthropic/claude-3-haiku`
- **上下文窗口**：20万 tokens
- **成本**：$0.00025/1K input tokens，$0.00125/1K output tokens
- **适用场景**：
  - ✅ 资源协调
  - ✅ 格式化输出
  - ✅ 简单文档生成

---

## 🔧 解决PDF文件读取问题

### 方案 1：使用 Gemini Pro 1.5（推荐）

**优点**：
- ✅ 支持100万token上下文，轻松处理大文件
- ✅ 成本低廉（比Claude便宜60%）
- ✅ 速度快

**实施步骤**：

1. **配置 OpenRouter**：
```yaml
# 在 .claude/config/model_config.yaml 中已配置
providers:
  openrouter:
    enabled: true
    api_key_env: "OPENROUTER_API_KEY"

models:
  long_context:
    primary:
      name: "google/gemini-pro-1.5"
      context_window: 1000000
```

2. **在代码中使用**：
```python
# 伪代码示例
if task == "material_intake":
    model = get_model("long_context.primary")  # 自动选择 Gemini Pro 1.5
    content = model.read_pdf(pdf_path)
```

### 方案 2：智能分块（Chunking）

如果单个模型仍然无法处理，使用智能分块：

```yaml
strategies:
  pdf_processing:
    smart_chunking:
      max_chunk_size: 100000  # tokens
      overlap: 1000  # 块之间重叠，保持上下文连贯
      model: "long_context.primary"
```

**工作流程**：
1. 将PDF分成多个块（每块10万tokens）
2. 每块之间有1000tokens重叠
3. 逐块读取和分析
4. 最后合并分析结果

### 方案 3：定向提取

只提取需要的章节：

```yaml
strategies:
  pdf_processing:
    targeted_extraction:
      steps:
        - "识别目标单元：Unit 1 Goldilocks"
        - "只提取第1-10页"
        - "使用reasoning模型分析"
```

---

## 💰 成本对比

### 当前方案（Claude API）
- 问题：文件太大，无法读取 ❌
- 成本：N/A（无法执行）

### 新方案（OpenRouter + Gemini）
| 任务 | 模型 | Tokens | 成本 |
|------|------|--------|------|
| 读取24MB教材PDF | Gemini Pro 1.5 | 150K input + 2K output | $0.20 |
| 课程分析 | Claude 3.5 Sonnet | 10K input + 3K output | $0.08 |
| 内容设计 | Claude 3.5 Sonnet | 8K input + 4K output | $0.08 |
| 大任务提议 | Claude 3.5 Sonnet | 6K input + 2K output | $0.05 |
| 活动设计 | Claude 3.5 Sonnet | 8K input + 5K output | $0.10 |
| 资源协调 | Claude 3 Haiku | 5K input + 2K output | $0.004 |
| 评估设计 | Claude 3.5 Sonnet | 8K input + 4K output | $0.08 |
| 质量审核 | Claude 3.5 Sonnet | 15K input + 3K output | $0.09 |
| 打包发布 | Claude 3 Haiku | 10K input + 6K output | $0.01 |
| **总计** | | | **≈ $0.67** |

**结论**：不到1美元（约5元人民币）完成一次完整的教学设计！

---

## 🎛️ 配置选项

### 成本敏感配置（最便宜）
适合预算有限的场景：

```yaml
# 修改 model_config.yaml
models:
  long_context:
    primary:
      name: "google/gemini-flash-1.5"  # 更便宜的版本
      cost_per_1k_tokens:
        input: 0.000075  # 超级便宜！
        output: 0.0003
  
  reasoning:
    primary:
      name: "anthropic/claude-3-sonnet"  # 而不是3.5
```

**预估成本**：约 $0.30/次

### 质量优先配置（最好效果）
适合重要教案设计：

```yaml
# 所有任务都使用最好的模型
models:
  long_context:
    primary:
      name: "google/gemini-pro-1.5"  # 大文件仍用Gemini
  
  reasoning:
    primary:
      name: "anthropic/claude-3.5-sonnet"  # 全部用3.5
  
  fast_execution:
    primary:
      name: "anthropic/claude-3.5-sonnet"  # 甚至简单任务也用最好的
```

**预估成本**：约 $1.20/次

### 平衡配置（推荐）
平衡成本和质量：

```yaml
# 这是默认配置
# 长文本用Gemini，核心设计用Claude 3.5，简单任务用Haiku
```

**预估成本**：约 $0.67/次

---

## 🛠️ 实施步骤

### 对于当前的PDF读取问题

**立即可以做的**：

1. **设置 OpenRouter API Key**：
```powershell
$env:OPENROUTER_API_KEY = "your-key"
```

2. **使用 Gemini Pro 1.5 读取PDF**：
在材料审核阶段，系统会自动：
```
检测到大文件 → 切换到 long_context.primary → 使用 Gemini Pro 1.5
```

3. **继续流程**：
材料读取完成后，后续阶段继续使用 Claude 进行高质量设计。

---

## 📊 监控和日志

系统会在 `state/LOG.md` 中记录模型使用情况：

```markdown
===== Material Intake =====
【使用模型】google/gemini-pro-1.5
【原因】大型PDF文件需要长上下文
【输入tokens】152,384
【输出tokens】1,856
【成本】$0.20
【状态】✅ 成功读取
```

---

## ❓ 常见问题

### Q1: 必须使用 OpenRouter 吗？
A: 不是必须的，但强烈推荐：
- OpenRouter 提供统一接口访问多种模型
- 支持 Gemini（100万token上下文）
- 成本透明，按使用付费

### Q2: 可以只用 Claude API 吗？
A: 可以，但有限制：
- Claude 最大上下文 20万tokens
- 单次请求大小有限制
- 对于24MB的PDF，需要分块处理

### Q3: Gemini 的质量如何？
A: 对于文本提取和理解，Gemini Pro 1.5 非常优秀：
- ✅ 长文本理解能力强
- ✅ 成本低廉
- ✅ 速度快
- ⚠️ 但推理能力不如 Claude 3.5 Sonnet

因此我们的策略是：
- 用 Gemini 读取和提取信息
- 用 Claude 3.5 进行教学设计和分析

### Q4: 如何控制成本？
A: 系统有多层成本控制：
1. 自动选择最合适的模型
2. 简单任务使用便宜模型
3. 缓存重复内容
4. 智能分块避免浪费

### Q5: 出错怎么办？
A: 系统有自动fallback机制：
```yaml
error_handling:
  - error: "request_too_large"
    action: "switch_to_long_context_model"
  - error: "context_length_exceeded"
    action: "apply_smart_chunking"
```

---

## 🎯 下一步行动

### 立即解决当前问题：

1. **获取 OpenRouter API Key**
   - 访问：https://openrouter.ai/
   - 注册并获取 key

2. **配置环境变量**
```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-..."
```

3. **重新运行教学设计流程**
```
/start-lesson-design Unit 1 Goldilocks and the three bears - Story time
```

系统会自动：
- ✅ 检测到大型PDF
- ✅ 切换到 Gemini Pro 1.5
- ✅ 成功读取教材
- ✅ 继续完成后续设计

---

## 📞 支持

如有问题，请查看：
- 配置文件：`.claude/config/model_config.yaml`
- 日志文件：`state/LOG.md`
- 错误信息会包含详细的调试信息

---

**总结**：通过配置 OpenRouter API 和使用 Gemini Pro 1.5，我们可以：
1. ✅ 解决大文件读取问题
2. ✅ 降低成本（$0.67/次完整设计）
3. ✅ 保持高质量（核心设计仍用 Claude 3.5）
4. ✅ 提升灵活性（根据任务选择最佳模型）
