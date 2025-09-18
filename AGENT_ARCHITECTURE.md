# 多代理博客写作架构

## 总览

仓库以 `/start-blog` 为唯一入口：协调器读取 `state/STATUS.yaml`，根据依赖调度 stylist → coordinator → researcher → outliner → writer → editor → publisher。最终交付 Markdown (`draft/post.md`) 与图像资产（`assets/` + `figures/*.meta.json`）。

## 代理矩阵与状态机

- `state/STATUS.yaml`：描述阶段（plan → research → outline → draft → review → publish）与守门条件。
- `/start-blog` 将按下表调度子代理并在 `state/LOG.md` 留痕：

| 阶段 | 子代理 | 主要职责 |
|------|--------|----------|
| Style Grounding | stylist | 复用或更新 `state/STYLE_PROFILE.md`，总结语气、节奏与常见修辞。 |
| Material Intake | coordinator | 梳理用户素材与限制，更新 `MATERIAL_AUDIT.md`、`PUBLISH_PLAN.md`。 |
| Research Deepdive | researcher | 归纳事实、补充链接，更新 `RESEARCH_SUMMARY.md`、`SOURCES.md`（Markdown 链接）。 |
| Outline Blueprint | outliner | 生成段落结构，指明每段所需事实/图片。 |
| Drafting Loop | writer | 在 `POST.md`、`draft/post.md` 完成草稿并嵌入 `![[assets/...]]` 图像占位。 |
| Editing Pass | editor | 人工审读风格与事实，记录反馈，必要时调用辅助脚本。 |
| Packaging Release | publisher | 核对 Markdown、图像与 `.meta.json`，更新日志并宣布 ready。 |

## 可选工具

- `optional-tools/src/blog_pipeline/`：历史脚本，可辅助提炼风格或检查引用；默认流程不依赖。
- `tools/run_stage.py`：列出 ready 任务或检查资产状态，不再强制校验 JSON 报告。

> 若调用脚本，请在 `state/LOG.md` 记录“命令 → 输出 → 是否采纳”，保持透明度。

## 与样例协同

- 样例文章集中在 `samples/example-articles/`，摘要见 `samples/README.md`。
- Stylist 默认沿用 `state/STYLE_PROFILE.md` 缓存；当样例更新或新增话题时，再总结并覆盖。
- Writer/ editor 应在开写前阅读相关样例，必要时在 `state/VOICE_AND_STRUCTURE.md` 补充语句示例与禁忌。

## 手动运行要点
1. 更新 `state/STATUS.yaml` 与 `docs/status.md`，确保 stage/依赖真实。
2. 逐阶段编辑 `state/` 文档，并在 `state/LOG.md` 记录时间、平台、负责人、要点。
3. 写作完成后，editor 在 `state/ITERATIONS.md` 标记反馈；publisher 核对 `assets/` 与 `figures/`，确认许可与说明完整。
4. 若使用辅助脚本（例如 `optional-tools/src/blog_pipeline/cli.py`），请注明用途并手动审阅结果。

## 守门条件（示例）
- Stylist 与 editor 在日志中签字确认语气一致。
- Researcher 或 writer 在 `state/SOURCES.md` 提供可访问链接，并在正文就近插入引用。
- Publisher 检查 `assets/` 与 `.meta.json` 成对存在、描述完整；若尚未提供图片，需在日志写明补交计划。

## 未来增强
- 结合多模态预览，自动校验图片是否就近引用。
- 构建反馈循环：根据读者互动数据更新 `STYLE_PROFILE.md` 与 `VOICE_AND_STRUCTURE.md`。
- 引入低门槛的图像生成或截图规范（Mermaid、Excalidraw 等），减少空 meta。

通过上述机制，团队可以在保持多代理自治的同时，维持文档化、可追溯的博客写作流程。
