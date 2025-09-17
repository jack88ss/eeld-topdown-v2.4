# Repository Guidelines

## Project Structure & Module Organization
- `src/blog_pipeline/`：已实现风格分析 (`style.py`)、草稿校验 (`check.py`)、文本指标工具 (`text_utils.py`)，其余模块（调研、提纲、草稿生成）待扩展。
- `state/`：多代理共享的事实源。
  - `STATUS.yaml` — 阶段与任务依赖（plan → research → outline → draft → review → publish）。
  - `STYLE_PROFILE.md` — 来源于示例文章的语气画像。
  - `MATERIAL_AUDIT.md` — 用户提供素材、限制与调研策略。
  - `RESEARCH_SUMMARY.md` — 事实摘要与引用矩阵。
  - `POST_OUTLINE.md` / `POST.md` — 大纲与工作稿。
  - `ITERATIONS.md` — 草稿版本、风格分、事实核查状态。
  - `LOG.md` — 命令、验证、平台交接日志。
- `draft/`：单一交付物 `post.md`（最终 Markdown），可直接粘贴到博客或 Obsidian。
- `figures/`：图像素材 `figure_<id>.png` 与 `.meta.json`（段落、用途、版权、更新时间）。
- `tools/run_stage.py`：读取 manifest，校验命名守卫，列出 ready 任务或触发命令。

## Build, Test, Development Commands
- 风格提炼：`python -m src.blog_pipeline.cli init-style --corpus /Users/wsy/Dropbox/example-blog-articles --output state/STYLE_PROFILE.md`
- 风格/事实校验：`python -m src.blog_pipeline.cli check --draft draft/post.md --profile state/STYLE_PROFILE.md --sources state/SOURCES.md`
- 其他阶段（素材审计、调研、提纲、撰写）暂由对应代理直接编辑 `state/` 文档完成，后续会增补 CLI 子命令以统一调度。
- 调度守卫：`python tools/run_stage.py [--stage <name>] [--run]`
- 测试占位：`pytest -q`（建成后需覆盖 style、research、outline、draft、editor 模块）。

## Orchestration & Review Workflow
- 每阶段结束更新 `state/STATUS.yaml`、`docs/status.md`、`state/LOG.md`。记录平台（Claude/Codex）、命令及退出码。
- `style_grounding` 任务完成前，不得进入调研；`style_match_score` 是编辑阶段守门条件。
- 当用户声明“仅用提供材料”时，在 `state/MATERIAL_AUDIT.md` 标记 `覆盖度: full`、`补充调研计划: 跳过`，并在 `state/LOG.md` 记录理由。
- 图像必须在首次提及段落附近插入 `![[assets/...]]`，并有 `.meta.json` 说明。发布前由 `publisher` 复核元数据（来源、版权、用途）。
- 编辑阶段需生成 `results/style_check.json` 与 `results/fact_check.log` 并写入 `state/ITERATIONS.md`；缺失事实引用必须补齐或删除对应内容。
- 若守门条件未达成，将任务状态设为 `blocked` 或 `needs_rerun`，并说明补救计划。

## Coding Style & Naming Conventions
- Python：4 空格缩进，类型注解，函数聚焦单一职责，必要时添加简短注释解释意图。
- Markdown：使用自然段，不滥用列表；引用格式 `[@key]` 与 `state/SOURCES.md` 对应；图片使用 Obsidian 语法 `![[assets/...]]`。
- 文件命名：`draft/post.md` 为最终稿；草稿中间版本可命名 `draft/post_v1.md`（需在 `state/ITERATIONS.md` 登记）。
- 结果文件：`results/style_check.json`、`results/fact_check.log`、`results/question_density.csv` 等；`tools/run_stage.py` 允许显式文件名或前缀 `style_`, `fact_`, `outline_`, `draft_`。

## Testing Guidelines
- `tests/` 下按模块建立文件（如 `test_style.py`, `test_outline.py`），输出 ≥80% 关键函数覆盖率。
- 对风格指标使用样例文章片段构建基准测试，确保设问/人称统计准确。
- 为事实校验编写单元测试，验证引用缺失时会返回错误并记录日志条目。

## Commit & Review Guidelines
- 使用 Conventional Commits，例如 `feat(blog): add style profile extractor`、`fix(editor): tighten fact check logging`。
- 在合并前更新：`state/ITERATIONS.md`、`state/LOG.md`、`docs/status.md`。
- PR 描述应概览：目标、涉及的状态文件、风格分/事实核查结果、待办项。

## Maintenance Notes
- 修改工作流需同时更新 `.claude/**`、`README.md`、`AGENT_ARCHITECTURE.md`、`CLAUDE.md`，保持自动化一致。
- 若新增 `.codex/` 配置，保证内容与 `.claude/` 镜像。
- 遇到失败或回滚，先记录到 `state/LOG.md`（含平台、命令、原因），再调整 `state/STATUS.yaml`。
- 图像策略：若生成或引用新图片，必须在 `.meta.json` 标注来源与许可；禁止将未授权素材提交到公开仓库。

## Dual-Agent Compatibility (Claude ↔ Codex)
- 两端共用同一套 `state/` 文档，禁止分叉。任何平台特定说明写入 `.claude/README.md` 或未来的 `.codex/README.md`，并在 `state/LOG.md` 引用。
- 官方命令统一使用 `python`, `pytest`, `tools/run_stage.py`；避免依赖仅某平台可用的指令。如需 Claude 专属 `/start-blog`，需提供 Codex 等效脚本并记录于日志。
- 若一端执行失败，记录失败命令与报错，在另一端执行补救操作前同步状态。

## 图像与素材
- 所有 `figure_<id>.png` 必须配套 `.meta.json`，包含：`paragraph`, `description`, `source`, `license`, `created_at`。
- 发布前请使用本地预览确认中文字符无乱码，必要时在 `.meta.json` 标明字体或截图来源。
- 如需自动生成图片（未来增强），记录使用的模型与提示词。

保持以上约定，可让多代理系统稳定地产出符合个人风格、事实准确的 Markdown 博客。
