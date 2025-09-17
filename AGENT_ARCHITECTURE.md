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

## 核心模块

### 已实现

- `src/blog_pipeline/style.py` — 扫描示例文章目录（默认 `/Users/wsy/Dropbox/example-blog-articles/`），统计句长、段落长度、问句/二人称频率与配图密度，写出结构化 `StyleProfile` 与 `state/STYLE_PROFILE.md`。
- `src/blog_pipeline/text_utils.py` — 提供段落/句子分割、指标分析与关键词提取函数，供风格提炼与校验复用。
- `src/blog_pipeline/check.py` — 依据 `StyleProfile` 计算 `style_match_score` 等指标，生成 `results/style_check.json`；同时扫描 Markdown 草稿的 `[@key]` 引用与外链，形成 `results/fact_check.log`。
- `src/blog_pipeline/cli.py` — 暴露 `init-style` 与 `check` 子命令，方便在 orchestrator 或 shell 中批量调用。

### 规划中

- `src/blog_pipeline/research.py` — 归并 `state/MATERIAL_AUDIT.md` 与外部检索结果，自动刷新 `state/RESEARCH_SUMMARY.md`、`state/SOURCES.md`。
- `src/blog_pipeline/outline.py` — 将风格画像与事实摘要转化为段落大纲，写入 `state/POST_OUTLINE.md`。
- `src/blog_pipeline/drafter.py` — 基于大纲输出初稿模板和图片占位。
- `src/blog_pipeline/editor.py` — 拓展风格匹配算法（如向量化），并结合事实检查返回可执行建议。
- CLI 其他子命令（`material` / `research` / `outline` / `draft` / `package`）将在上述模块落地后补充，以便全流程脚本化。

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
1. 运行 `python -m src.blog_pipeline.cli init-style ...` 生成或刷新 `state/STYLE_PROFILE.md`。
2. 由各角色直接编辑 `state/MATERIAL_AUDIT.md`、`state/RESEARCH_SUMMARY.md`、`state/POST_OUTLINE.md`、`state/POST.md` 等文件，并同步 `state/STATUS.yaml`、`state/LOG.md`。
3. 写作阶段结束后执行 `python -m src.blog_pipeline.cli check ...` 产出风格/事实报告，满足守门条件后进入发布。
4. 使用 `python tools/run_stage.py` 观察 ready 任务或触发 manifest 中预配置命令。

## 未来增强
- 训练风格分类器，提高相似度评估可信度。
- 集成图像生成/检索代理，为缺失素材自动补画面。
- 构建反馈回路：根据读者互动数据更新 `STYLE_PROFILE.md`。
- 推出多版本打包（长文/摘要/社媒短帖），共享调研成果。

通过以上改造，仓库正式转型为“主题输入 → Markdown 博客” 的多代理写作平台。
