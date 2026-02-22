# 大文件读取实际解决方案

> **当前情况**：OpenRouter API Key 已配置，但系统仍使用默认的文件读取工具

---

## 🎯 问题分析

**终端日志显示**：
```
Read(materials\textbooks\译林版五上英语电子课本.pdf)
⎿ Read PDF (24.1MB)
⎿ API Error: 413 {"error":{"type":"request_too_large","message":"Request exceeds the maximum size"}}
```

**原因**：
- Cursor/Claude 的 `Read` 工具直接调用 Anthropic API
- 即使配置了 OpenRouter，默认工具仍使用 Claude API
- 24MB 的 PDF 超过了单次请求限制

---

## ✅ 立即可用的解决方案

### 方案 1：提取关键章节文本（推荐，5分钟）⭐

**步骤**：

1. **打开 PDF 教材**
   - 找到 Unit 1 Goldilocks and the three bears 的页面

2. **复制相关内容**
   - 复制 Story time 部分的课文
   - 复制教学目标、重难点
   - 复制词汇表

3. **保存为文本文件**
   ```powershell
   # 创建文本文件
   notepad materials\textbooks\unit1_goldilocks.txt
   ```

4. **粘贴内容并保存**
   ```
   Unit 1 Goldilocks and the three bears - Story time
   
   【Story】
   Goldilocks is in the forest. She sees a house.
   ...（粘贴课文内容）
   
   【Vocabulary】
   house, room, hungry, thirsty, tired, bear, forest, soup...
   
   【Grammar】
   There is / There are ...
   
   【Teaching Objectives】
   1. Students can understand the story
   2. Students can use "There is/are" sentences
   ...
   ```

5. **重新启动设计**
   ```powershell
   /start-lesson-design "Unit 1 Goldilocks and the three bears - Story time" "五年级" "译林版"
   ```

**优点**：
- ✅ 立即可用，无需额外配置
- ✅ 提取的内容更精准，针对本节课
- ✅ 避免处理整本教材的冗余信息

---

### 方案 2：使用教师用书的文本版（如果有）

**步骤**：

1. **检查是否有教师用书的文本版本**
   ```powershell
   ls materials\textbooks\*.txt
   ls materials\textbooks\*.md
   ```

2. **如果有Word版本，转换为文本**
   - 如果有 `.docx` 版本，打开并另存为 `.txt`

3. **使用文本文件启动**

---

### 方案 3：分步提取（针对特定单元）

创建一个简化的教材摘要：

```powershell
# 创建摘要文件
notepad materials\textbooks\unit1_summary.txt
```

**内容模板**：
```
=== Unit 1 Goldilocks and the three bears ===

【课型】Story time

【Story Text】
（粘贴故事原文）

【Key Vocabulary】
house, room, hungry, thirsty, tired
forest, soup, hard, soft, just right
bear, afraid

【Key Sentences】
There is a house in the forest.
There are three bears in front of her.
This soup is too hot/cold/just right.

【Grammar Focus】
There is + 单数名词
There are + 复数名词

【Teaching Objectives】
（从教师用书复制）

【Teaching Key Points】
（从教师用书复制）

【Teaching Difficulties】
（从教师用书复制）
```

---

### 方案 4：使用课程标准Word文档

**注意到课标文档也读取失败**：
```
Read(materials\standards\4义务教育英语课程标准（2022年版）.docx)
⎿ Error reading file
```

**解决**：
```powershell
# 将Word文档另存为文本文件
# 1. 打开Word文档
# 2. 另存为 → 纯文本 (.txt)
# 3. 保存到 materials\standards\课程标准.txt
```

---

## 🚀 推荐工作流程

### 完整的快速启动流程：

```powershell
# 1. 创建 Unit 1 文本摘要
notepad materials\textbooks\unit1_goldilocks.txt

# 2. 粘贴以下内容（最小化版本）：
```

**最小化文本内容**：
```
Unit 1 Goldilocks and the three bears - Story time
译林版小学英语五年级上册

【Story】
Goldilocks is in the forest. She is hungry and thirsty.
She sees a house. There is some soup on the table.
This soup is too hot. This soup is too cold. 
This soup is just right.

There are three beds in the room.
This bed is too hard. This bed is too soft.
This bed is just right.

There are three bears in front of her!
Help! Help! Goldilocks runs away.

【Key Vocabulary】
- house (房子)
- room (房间)  
- forest (森林)
- hungry (饥饿的)
- thirsty (口渴的)
- tired (累的)
- soup (汤)
- hard (硬的)
- soft (软的)
- just right (正合适)
- bear (熊)
- in front of (在...前面)
- afraid (害怕的)

【Key Grammar】
There is + 单数名词
There are + 复数名词

Examples:
- There is a house in the forest.
- There are three beds in the room.
- There are three bears in front of her.

【Grade Level】五年级上册
【Lesson Type】Story time  
【Duration】40分钟
```

```powershell
# 3. 保存文件

# 4. 重新启动
/start-lesson-design "Unit 1 Goldilocks and the three bears - Story time" "五年级" "译林版"
```

---

## 💡 为什么这样有效？

1. **精准内容**：只包含本节课需要的内容
2. **文件小**：几KB的文本文件，轻松读取
3. **结构清晰**：已经组织好的信息，更高效
4. **立即可用**：无需复杂配置

---

## 📊 后续流程

文本文件准备好后，系统会：

1. ✅ 成功读取 `unit1_goldilocks.txt`
2. ✅ 分析课文内容、词汇、语法
3. ✅ 提出核心大任务建议（例如："改编和表演Goldilocks故事"）
4. ⏸️ 暂停，等待您确认大任务
5. ✅ 继续完成活动设计、资源协调、评估设计
6. ✅ 生成完整教案 + 预习清单 + 作业纸

---

## 🎯 立即行动

**现在就做（3分钟）**：

```powershell
# 1. 创建文本文件
notepad materials\textbooks\unit1_goldilocks.txt

# 2. 复制上面的"最小化文本内容"

# 3. 粘贴到记事本并保存

# 4. 关闭当前流程（如果还在运行）

# 5. 重新启动
/start-lesson-design "Unit 1 Goldilocks and the three bears - Story time" "五年级" "译林版"
```

---

## ❓ 常见问题

### Q: 为什么不直接使用 OpenRouter？
A: 在当前的 Cursor/Claude 环境中：
- 文件读取由 Cursor 的系统工具完成
- 这些工具默认使用 Claude API
- 要使用 OpenRouter 需要通过 MCP (Model Context Protocol) 或自定义工具
- 提取文本是最快速、最可靠的方法

### Q: OpenRouter 配置白费了吗？
A: 不是！OpenRouter 配置可以用于：
- 未来的自定义工具开发
- 直接的 API 调用场景
- 其他需要长上下文的任务

### Q: 需要提取整本教材吗？
A: **不需要！** 只需要：
- 本节课的课文（Story time）
- 相关词汇和句型
- 教学目标（如果有）
- 大约 1-2 页的内容即可

### Q: 教师用书也需要提取吗？
A: 如果教师用书有关于这个单元的：
- 教学建议
- 重难点分析
- 活动设计示例

可以提取这部分内容到同一个文本文件中。

---

## ✅ 成功标志

当您看到：
```
Read(materials\textbooks\unit1_goldilocks.txt)
⎿ Read 50 lines
✅ 成功读取
```

说明已经成功！系统会继续完成后续步骤。

---

**下一步**：创建文本摘要文件并重新启动！ 🚀
