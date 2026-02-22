# PDF文件读取指南 - 处理大型教材文件

> 解决 "Request exceeds the maximum size" 错误

---

## 🚨 问题场景

执行教学设计流程时遇到：

```
Read(materials\textbooks\译林版五上英语电子课本.pdf)
⎿ Read PDF (24.1MB)
⎿ API Error: 413 {"error":{"type":"request_too_large","message":"Request exceeds the maximum size"}}
```

---

## 💡 解决方案总览

### 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **方案1：使用长上下文模型** | ✅ 简单直接<br>✅ 成本低<br>✅ 效果好 | ⚠️ 需要配置OpenRouter | ⭐⭐⭐⭐⭐ |
| 方案2：智能分块 | ✅ 不需额外配置 | ⚠️ 复杂<br>⚠️ 可能遗漏信息 | ⭐⭐⭐ |
| 方案3：手动提取关键页 | ✅ 精确控制 | ❌ 手工操作<br>❌ 不可自动化 | ⭐⭐ |

---

## 🎯 推荐方案：使用 Gemini Pro 1.5

### 为什么选择 Gemini Pro 1.5？

| 特性 | Claude 3.5 Sonnet | Gemini Pro 1.5 | 差异 |
|------|-------------------|----------------|------|
| 上下文窗口 | 200K tokens | **1M tokens** | 🔥 5倍 |
| 单文件大小 | 约30MB限制 | **150MB+** | 🔥 轻松处理 |
| 输入成本 | $3.00/1M tokens | **$1.25/1M tokens** | 💰 便宜60% |
| 输出成本 | $15.00/1M tokens | **$5.00/1M tokens** | 💰 便宜67% |
| 速度 | 快 | **更快** | ⚡ |
| 质量 | 优秀（推理） | 优秀（理解） | 各有所长 |

**结论**：对于读取和理解教材，Gemini Pro 1.5 是完美选择！

---

## 🚀 快速配置（5分钟）

### 步骤 1：注册 OpenRouter（1分钟）

1. 访问 https://openrouter.ai/
2. 点击 "Sign Up" 注册账号
3. 登录后点击 "Keys" 标签
4. 点击 "Create Key" 创建 API Key
5. 复制 API Key（以 `sk-or-v1-` 开头）

💰 **免费额度**：OpenRouter 提供 $5 免费额度，够用几十次！

### 步骤 2：配置环境变量（1分钟）

**Windows PowerShell**:
```powershell
# 设置环境变量（永久）
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-你的key', 'User')

# 验证设置
echo $env:OPENROUTER_API_KEY

# 如果上面不生效，临时设置：
$env:OPENROUTER_API_KEY = "sk-or-v1-你的key"
```

**Linux/Mac**:
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export OPENROUTER_API_KEY="sk-or-v1-你的key"' >> ~/.bashrc
source ~/.bashrc

# 验证
echo $OPENROUTER_API_KEY
```

### 步骤 3：重启终端（1分钟）

关闭并重新打开终端/PowerShell，确保环境变量生效。

### 步骤 4：重新运行（2分钟）

```bash
/start-lesson-design Unit 1 Goldilocks and the three bears - Story time
```

系统会自动：
1. 检测到大型PDF文件
2. 切换到 Gemini Pro 1.5 模型
3. 成功读取教材
4. 继续完成设计流程

---

## 🔍 工作原理

### 自动模型切换机制

```
┌─────────────────────────────────┐
│  尝试读取 PDF 文件              │
└────────────┬────────────────────┘
             ↓
        检测文件大小
             ↓
    ┌────────┴────────┐
    │                 │
24MB > 限制         24MB < 限制
    │                 │
    ↓                 ↓
切换到            使用默认
Gemini Pro 1.5    Claude API
    │                 │
    └────────┬────────┘
             ↓
       成功读取 ✅
```

### 代码实现逻辑（伪代码）

```python
def read_material(file_path):
    file_size = get_file_size(file_path)
    
    if file_size > 20MB:
        # 使用长上下文模型
        model = "google/gemini-pro-1.5"
        api = OpenRouterAPI(api_key=env.OPENROUTER_API_KEY)
    else:
        # 使用默认模型
        model = "anthropic/claude-3.5-sonnet"
        api = AnthropicAPI(api_key=env.ANTHROPIC_API_KEY)
    
    try:
        content = api.read_pdf(file_path, model=model)
        log_usage(model, tokens, cost)
        return content
    except RequestTooLarge:
        # 降级到智能分块
        return read_with_chunking(file_path)
```

---

## 💰 成本详解

### 实际案例：译林版五上英语教材

**文件信息**：
- 文件名：`译林版五上英语电子课本.pdf`
- 文件大小：24.1 MB
- 预估页数：约100页
- 预估tokens：约150,000 tokens

**使用 Gemini Pro 1.5 成本**：
```
输入成本：150,000 tokens × $1.25/1M = $0.1875
输出成本（摘要）：2,000 tokens × $5.00/1M = $0.01
总计：约 $0.20（约1.4元人民币）
```

**如果使用 Claude 3.5 Sonnet（假设能读取）**：
```
输入成本：150,000 tokens × $3.00/1M = $0.45
输出成本：2,000 tokens × $15.00/1M = $0.03
总计：约 $0.48（约3.4元人民币）
```

**节省**：$0.28（约2元人民币），便宜 **58%**！

### 完整教学设计流程成本

| 阶段 | 模型 | 成本 |
|------|------|------|
| 材料审核（读取PDF） | Gemini Pro 1.5 | $0.20 |
| 课程分析 | Claude 3.5 Sonnet | $0.08 |
| 内容设计 | Claude 3.5 Sonnet | $0.08 |
| 大任务提议 | Claude 3.5 Sonnet | $0.05 |
| 活动设计 | Claude 3.5 Sonnet | $0.10 |
| 资源协调 | Claude 3 Haiku | $0.004 |
| 评估设计 | Claude 3.5 Sonnet | $0.08 |
| 质量审核 | Claude 3.5 Sonnet | $0.09 |
| 打包发布 | Claude 3 Haiku | $0.01 |
| **总计** | | **$0.69** |

**不到5元人民币完成一份完整的专业教学设计！**

---

## 📊 日志示例

系统会在 `state/LOG.md` 中详细记录：

```markdown
===== 2026-01-17T14:30:00Z | Material Intake =====
【Orchestrator 登场】
检测到大型PDF文件需要处理。

【文件信息】
- 文件：译林版五上英语电子课本.pdf
- 大小：24.1 MB
- 预估tokens：150,000

【模型选择】
- 原始模型：anthropic/claude-3.5-sonnet
- 检测到大文件，切换模型
- 最终模型：google/gemini-pro-1.5
- 原因：支持100万token上下文，成本更低

【读取进度】
- 开始读取：14:30:05
- 完成读取：14:30:42
- 耗时：37秒
- 状态：✅ 成功

【Token使用】
- 输入tokens：152,384
- 输出tokens：1,856
- 总计：154,240 tokens

【成本统计】
- 输入成本：$0.19
- 输出成本：$0.01
- 总成本：$0.20

【提取内容】
- 识别单元：Unit 1 Goldilocks and the three bears
- 核心词汇：house, room, hungry, thirsty, tired...
- 核心句型：There is/are...
- 学习目标：理解故事，学习There be句型

【Orchestrator 退场】
材料审核完成，进入课程分析阶段。
```

---

## 🛠️ 高级配置

### 自定义模型选择

编辑 `.claude/config/model_config.yaml`：

```yaml
# 如果想用更便宜的模型
models:
  long_context:
    primary:
      name: "google/gemini-flash-1.5"  # 更便宜！
      cost_per_1k_tokens:
        input: 0.000075  # 仅 $0.075/1M tokens
        output: 0.0003
      notes: "极其便宜，速度更快，但略微降低质量"
```

### 智能分块策略

如果单个文件仍然太大：

```yaml
strategies:
  pdf_processing:
    smart_chunking:
      enabled: true
      max_chunk_size: 100000  # 每块10万tokens
      overlap: 1000  # 块之间重叠1000tokens
      model: "google/gemini-pro-1.5"
```

---

## ❓ 常见问题

### Q1: OpenRouter 安全吗？
A: **是的**，非常安全：
- OpenRouter 是正规的 API 聚合服务
- 使用标准的 OAuth 和 API Key 认证
- 不存储您的数据
- 支持主流模型提供商（Google、Anthropic、OpenAI等）

### Q2: 必须付费吗？
A: **不是**：
- OpenRouter 提供 **$5 免费额度**
- $5 可以完成约 7-8 次完整的教学设计
- 足够试用和评估

### Q3: 如果不想配置 OpenRouter，有其他办法吗？
A: **有的**，但效果较差：

**方案 A：手动分块**
1. 将PDF导出为文本文件
2. 手动分成多个小文件
3. 分别上传和分析

**方案 B：只提取关键页面**
1. 识别需要的单元（如 Unit 1）
2. 只复制相关页面到新PDF
3. 上传小文件

**方案 C：使用在线PDF工具**
1. 使用 PDF.ai 或类似服务
2. 上传PDF并提取文本
3. 复制文本到系统

但这些方案都：
- ❌ 需要手动操作
- ❌ 效率低
- ❌ 可能遗漏信息
- ❌ 不可自动化

**推荐还是配置 OpenRouter**！

### Q4: Gemini 的质量真的够用吗？
A: **对于读取理解，完全够用**：

| 任务类型 | Gemini Pro 1.5 | Claude 3.5 Sonnet |
|---------|----------------|-------------------|
| 文本提取 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 长文本理解 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 信息定位 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 复杂推理 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 创意生成 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**我们的策略**：
- 用 **Gemini** 读取和提取教材信息（便宜、快速、准确）
- 用 **Claude 3.5** 进行教学设计和分析（最强推理能力）

这样既节省成本，又保证质量！

### Q5: 如何查看实际使用的模型？
A: 查看 `state/LOG.md`：

```markdown
【模型选择】
- 最终模型：google/gemini-pro-1.5
- 原因：支持100万token上下文

【Token使用】
- 输入tokens：152,384
- 输出tokens：1,856

【成本统计】
- 总成本：$0.20
```

---

## 🎯 立即行动

### 现在就解决您的PDF读取问题：

1. **获取 OpenRouter API Key** （2分钟）
   👉 https://openrouter.ai/keys

2. **设置环境变量** （1分钟）
   ```powershell
   [System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-你的key', 'User')
   ```

3. **重启终端** （30秒）

4. **重新运行** （自动完成）
   ```
   /start-lesson-design Unit 1 Goldilocks and the three bears - Story time
   ```

✅ **就这么简单！**

---

## 📞 需要帮助？

遇到问题请查看：
- 📖 完整配置指南：`.claude/config/MULTI_MODEL_SETUP.md`
- 📋 模型配置文件：`.claude/config/model_config.yaml`
- 📝 执行日志：`state/LOG.md`

---

**总结**：
- ✅ 配置 OpenRouter + Gemini Pro 1.5
- ✅ 5分钟完成配置
- ✅ $5 免费额度
- ✅ 轻松处理大型PDF
- ✅ 成本降低60%
- ✅ 速度更快

**让我们开始吧！** 🚀
