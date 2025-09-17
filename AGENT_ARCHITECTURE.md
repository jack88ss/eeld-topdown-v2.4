# 多代理博客写作架构

## 总览

系统复用了原论文项目的自动化骨架，但将目标改为**长篇中文博客**。我们沿用 Claude Code / Codex 的多代理能力，实现“风格 → 资料 → 大纲 → 草稿 → 编辑 → 发布”的串并结合流程，并保证唯一产出是 `draft/post.md` 与配套图片。

## 代理矩阵与状态机

- 状态机：`state/STATUS.yaml` 描述阶段（plan → research → outline → draft → review → publish）、任务依赖与守门条件（风格分 ≥0.85、事实核查完成、图像就位）。
- `/start-blog`（待实现）或 `python tools/run_stage.py` 将读取 manifest，调度下列子代理：

| 阶段 | 子代理 | 主要职责 |
|------|--------|----------|
| Style Grounding | `stylist` | 分析示例文章，产出 `state/STYLE_PROFILE.md` 指标（句长、设问密度、二人称频率、图像节奏等）。 |
| Material Intake | `coordinator` | 整理用户主题与材料，更新 `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md`，决定是否需要外部调研。 |
| Research Deepdive | `researcher` | 组合用户素材与在线检索，输出 `state/RESEARCH_SUMMARY.md`、`state/SOURCES.md`，并标注引用可信度。 |
| Outline Blueprint | `outliner` | 将风格画像与事实摘要转化为模块化段落大纲，维护 `state/POST_OUTLINE.md`。 |
| Drafting Loop | `writer` | 按大纲撰写 `state/POST.md` 与 `draft/post.md`，插入 `![[assets/...]]` 图像，占位引用。 |
| Editing Pass | `editor` | 执行风格/事实检查，生成 `results/style_check.json`、`results/fact_check.log`，更新 `state/ITERATIONS.md`。 |
| Packaging Release | `publisher` | 审核 `.meta.json`、整理图像与 Markdown，宣告发布完成。 |

代理之间通过 `state/LOG.md` 留痕，保证 Codex 与 Claude 互相接力时拥有完整上下文。

## 核心模块（计划实现）

### `src/blog_pipeline/style.py`
- 读取样例目录 `/Users/wsy/Dropbox/example-blog-articles/`。
- 统计平均段落长度、问句/第二人称比例、比喻词、图像密度。
- 输出 `state/STYLE_PROFILE.md` 并返回结构化 profile。

### `src/blog_pipeline/research.py`
- 聚合 `state/MATERIAL_AUDIT.md` 中的素材与外部搜索结果。
- 生成 `state/RESEARCH_SUMMARY.md` 表格（官方/媒体/用户/数据分类），同步引用到 `state/SOURCES.md`。
- 在用户禁止调研时，记录“仅使用提供材料”。

### `src/blog_pipeline/outline.py`
- 根据 profile + summary 生成 `Outline` 数据结构，包含模块顺序、段落要点、所需图像。
- 写入 `state/POST_OUTLINE.md`，支持记录定制模块。

### `src/blog_pipeline/drafter.py`
- 将 Outline 转换为 Markdown 草稿模版，在每个段落注入语气提醒。
- 插入图片占位（`![[assets/...]]`）并预留 `.meta.json` TODO。

### `src/blog_pipeline/editor.py`
- 计算草稿与 profile 的余弦相似度、设问密度、第二人称频率。
- 汇总事实句并验证是否存在 `[@ref]` 或材料链接。
- 产出 `StyleReport` 与 `FactReport`，写入 `results/`。

### `src/blog_pipeline/cli.py`
- 提供 `init-style`、`material`、`research`、`outline`、`draft`、`check`、`package` 子命令，供 orchestrator 或用户调用。
- 支持 `--dry-run` 与 `--use-provided-only` 等开关，满足“仅用用户材料”场景。

## 改造与差异
1. **输出重构**：弃用 Typst/PDF/Word，仅保留 Markdown + 图像元数据。
2. **风格优先**：新增 `STYLE_PROFILE.md` 与风格评分守门条件，确保文章贴近作者语气。
3. **事实检查日志**：`results/fact_check.log` 取代原先的统计验证文件。
4. **任务命名更贴博客**：`state/STATUS.yaml` 中的任务改为 style/material/research/outline/draft/review/publish。
5. **素材审计**：`state/MATERIAL_AUDIT.md` 替代数据审计，强调用户材料、版权与禁区。

## 使用方式

### 自动模式（待实现）
```
/start-blog <主题> [--materials <路径或URL列表>] [--no-research]
```
- 解析状态机 → 并发执行无依赖任务。
- 根据材料密度决定是否触发 `researcher`。
- 迭代直到 `packaging_release` 输出最终 Markdown。

### 手动模式（当前）
1. `python -m src.blog_pipeline.cli init-style ...`
2. 更新 `state/MATERIAL_AUDIT.md`，运行 `tools/run_stage.py` 查看下一任务。
3. 按阶段执行 `research` / `outline` / `draft` / `check` / `package`。
4. 每次命令结束后在 `state/STATUS.yaml` 与 `state/LOG.md` 更新状态。

## 未来增强
- 训练风格分类器，提高相似度评估可信度。
- 集成图像生成/检索代理，为缺失素材自动补画面。
- 构建反馈回路：根据读者互动数据更新 `STYLE_PROFILE.md`。
- 推出多版本打包（长文/摘要/社媒短帖），共享调研成果。

通过以上改造，仓库正式转型为“主题输入 → Markdown 博客” 的多代理写作平台。
