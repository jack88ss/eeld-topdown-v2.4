# 项目重命名指南

## 当前状态

**当前目录名**：`agent-end-to-end-blog-writing`  
**建议新名称**：`elementary-english-lesson-designer`

---

## 为什么要重命名？

当前的目录名 `agent-end-to-end-blog-writing` 反映的是项目的原始用途（博客写作），但项目已经完全改造为**小学英语教学设计专家系统**，因此需要一个更贴切的名称。

---

## 建议的新名称

### 首选方案 ⭐⭐⭐⭐⭐
**`elementary-english-lesson-designer`**

**优点**：
- ✅ 准确反映项目功能（小学英语教学设计）
- ✅ 专业、国际化
- ✅ 易于理解和记忆
- ✅ SEO友好
- ✅ 符合GitHub命名规范

**缩写**：EELD

---

## 重命名步骤

### 方法1：直接重命名目录（推荐）

#### Windows (PowerShell)
```powershell
# 1. 进入父目录
cd C:\Users\Administrator\Desktop\myproject

# 2. 重命名目录
Rename-Item "agent-end-to-end-blog-writing" "elementary-english-lesson-designer"

# 3. 进入新目录
cd elementary-english-lesson-designer
```

#### Linux / macOS
```bash
# 1. 进入父目录
cd ~/projects

# 2. 重命名目录
mv agent-end-to-end-blog-writing elementary-english-lesson-designer

# 3. 进入新目录
cd elementary-english-lesson-designer
```

---

### 方法2：Git仓库重命名

如果项目已经是Git仓库：

```bash
# 1. 进入项目目录
cd agent-end-to-end-blog-writing

# 2. 更新远程仓库名称（在GitHub上操作）
# Settings -> Repository name -> 修改为 elementary-english-lesson-designer

# 3. 更新本地远程URL
git remote set-url origin https://github.com/your-username/elementary-english-lesson-designer.git

# 4. 退出目录并重命名
cd ..
mv agent-end-to-end-blog-writing elementary-english-lesson-designer
cd elementary-english-lesson-designer

# 5. 验证
git remote -v
```

---

### 方法3：创建新目录并复制（安全方法）

```bash
# 1. 创建新目录
mkdir elementary-english-lesson-designer

# 2. 复制所有文件（排除.git）
cp -r agent-end-to-end-blog-writing/* elementary-english-lesson-designer/
cp -r agent-end-to-end-blog-writing/.claude elementary-english-lesson-designer/

# 3. 验证文件完整性
cd elementary-english-lesson-designer
ls -la

# 4. 确认无误后删除旧目录（可选）
# cd ..
# rm -rf agent-end-to-end-blog-writing
```

---

## 重命名后需要更新的地方

### 1. 文档内部引用 ✅（已完成）
以下文件已经更新：
- [x] README.md
- [x] PROJECT_INFO.md（新建）
- [x] TRANSFORMATION_SUMMARY.md
- [x] 其他文档中的项目名称引用

### 2. Git配置（如果使用Git）
```bash
# 检查远程仓库URL
git remote -v

# 如果需要更新
git remote set-url origin https://github.com/your-username/elementary-english-lesson-designer.git
```

### 3. IDE/编辑器配置
- VS Code: 更新工作区设置中的路径
- Cursor: 重新打开项目目录
- 其他编辑器: 更新项目路径

### 4. 环境变量（如果有）
检查是否有使用项目路径的环境变量，需要相应更新。

---

## 验证清单

重命名后请检查：

- [ ] 目录名称已更改
- [ ] 项目可以正常打开
- [ ] 所有文件都在新目录中
- [ ] Git历史保留（如果使用Git）
- [ ] 文档中的项目名称已更新
- [ ] 命令可以正常运行：`/start-lesson-design`
- [ ] 所有配置文件路径正确

---

## 推荐操作

### 立即执行（安全且简单）

在Windows PowerShell中：

```powershell
# 当前位置：项目内部
cd ..

# 重命名
Rename-Item "agent-end-to-end-blog-writing" "elementary-english-lesson-designer"

# 确认
ls

# 重新进入
cd elementary-english-lesson-designer

# 验证
ls
```

**预计耗时**：< 1分钟  
**风险等级**：🟢 低（只是重命名，不修改内容）

---

## 其他命名选项（备选）

如果不喜欢 `elementary-english-lesson-designer`，还可以考虑：

### 选项2：简短版
**`english-lesson-designer`**
- 更简短
- 仍然清晰

### 选项3：通用版
**`ai-lesson-designer`**
- 可扩展到其他学科
- 更通用

### 选项4：中文拼音
**`xiaoxue-yingyu-jiaoan`**
- 中文友好
- 但国际化程度低

### 选项5：缩写
**`eeld-system`**
- Elementary English Lesson Designer
- 简洁但不够直观

---

## 常见问题

### Q1: 重命名会影响项目功能吗？
**A**: 不会。项目功能完全不受影响，只是目录名称改变。

### Q2: 需要更新代码吗？
**A**: 不需要。所有配置都使用相对路径，不依赖目录名称。

### Q3: Git历史会丢失吗？
**A**: 不会。目录重命名不影响Git历史。

### Q4: 如果重命名后有问题怎么办？
**A**: 可以再次重命名回原来的名称，没有任何损失。

### Q5: 必须现在重命名吗？
**A**: 不是必须，但建议尽早重命名，以避免以后的混淆。

---

## 建议行动

**推荐做法**：
1. ✅ 立即重命名为 `elementary-english-lesson-designer`
2. ✅ 验证项目功能正常
3. ✅ 如果使用Git，更新远程仓库名称
4. ✅ 更新个人文档/笔记中的项目引用

**预计总耗时**：5-10分钟

---

## 重命名后的项目结构

```
elementary-english-lesson-designer/
├── .claude/
│   ├── agents/           # 7个代理配置
│   ├── commands/         # 启动命令
│   └── settings.json     # 权限配置
├── state/                # 状态和设计文档
├── draft/                # 生成的教案
├── samples/              # 教学设计样例
├── assets/               # 教学资源
├── README.md            # 项目说明（已更新）
├── PROJECT_INFO.md      # 项目信息（新建）
├── RENAME_GUIDE.md      # 本文件
└── ...
```

---

**建议新名称**：`elementary-english-lesson-designer`  
**缩写**：EELD  
**推荐度**：⭐⭐⭐⭐⭐

---

**准备好了吗？让我们一起完成这个简单的重命名！** 🚀
