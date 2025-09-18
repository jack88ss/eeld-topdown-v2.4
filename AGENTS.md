# Repository Guidelines

## Project Structure & Module Organization
- 推荐入口：`/start-blog <主题>`（Claude Code 或镜像 orchestrator），协调 stylist → coordinator → researcher → outliner → writer → editor → publisher。
- `state/`：流程事实源，需随阶段同步。
  - `STATUS.yaml` — 任务图与守门条件。
  - `STYLE_PROFILE.md` — 风格缓存（默认沿用）；当样例更新时刷新。
  - `MATERIAL_AUDIT.md`、`RESEARCH_SUMMARY.md`、`PUBLISH_PLAN.md` — 记录素材、事实、节奏与风险。
  - `POST_OUTLINE.md`、`POST.md` — 大纲与草稿正文。
  - `ITERATIONS.md` — 草稿版本、反馈、后续计划。
  - `LOG.md` — 每个阶段结束后的时间戳、负责人、关键信息。
- `assets/` + `figures/`：配图与 `.meta.json` 描述（paragraph、description、source、license、captured_at）。
- `samples/example-articles/`：风格样例及索引（见 `samples/README.md`）。
- `optional-tools/`：如需脚本或测试，可集中放置；运行前请在 `state/LOG.md` 说明目的。

## 协作原则
- `/start-blog` 负责解析状态机、触发子代理、检查守门条件并统一汇报；手动执行时需保持同样的文件与日志同步节奏。
- Stylist / writer / editor 以人工判断为主，若调用脚本辅助（如风格检查），须在 `state/LOG.md` 写明命令、输出与采纳结论。
- 关键操作（新增素材、更新大纲、审阅结果、发布打包）必须更新 `state/LOG.md`，并在 `docs/status.md` 概览最新状态。
- `tools/run_stage.py` 仅用于查看 ready 任务或进行轻量资产检查，不再强制校验 JSON 报告。

## Orchestration & Review Workflow
1. **stylist**：
   - 若 `state/STYLE_PROFILE.md` 仍适用，记录“沿用缓存”；
   - 样例更新时，阅读 `samples/example-articles/`，总结语气/结构要点并更新缓存。
2. **coordinator**：整理用户输入与限制，更新 `MATERIAL_AUDIT.md`、`PUBLISH_PLAN.md`，标明是否允许外部调研。
3. **researcher**：归纳事实，补充链接，使用普通 Markdown 列表更新 `RESEARCH_SUMMARY.md` 与 `SOURCES.md`。
4. **outliner**：编写模块化大纲，指出每段的图像/引用需求。
5. **writer**：在 `POST.md` 形成完整草稿，确保段落顺畅、问句频率充足，并嵌入 `![[assets/figure_01.png]]` 等图片占位。
6. **editor**：人工审读风格与事实；如运行辅助脚本，请记录命令与是否采纳。将结论写入 `ITERATIONS.md` 与 `LOG.md`。
7. **publisher**：核对 Markdown、图片与 `.meta.json`，确认外链可访问及版权状态；在日志中盖章“ready for publish”。

## Writing & Naming Guidelines
- Markdown：以自然段叙述为主，链接写为 `[标题](URL)` 或脚注；避免 `[@key]` 格式。
- 图片：命名 `figure_01.png` 等，与 `.meta.json` 配对，正文说明需紧邻首次引用段落。
- 草稿命名：内部草稿使用 `state/POST.md`，对外版本固定 `draft/post.md`；如需留档可在日志或 `ITERATIONS.md` 标注版本号。
- 引用：`state/SOURCES.md` 使用普通列表，含标题、来源、日期、链接、简要说明。

## Optional Automation
- 若需要批量指标或事实校验，可在 `optional-tools/` 创建脚本；运行前后需在 `state/LOG.md` 记录目的、命令、输出以及是否采纳结果。
- `optional-tools/README.md`（待补）应说明依赖与用法，避免误用。

## Maintenance Notes
- 调整流程或守门条件时，须同步更新 `.claude/**`、`README.md`、`AGENT_ARCHITECTURE.md`、`CLAUDE.md`，保证自动化与文档一致。
- 若添加 `.codex/` 或其他平台配置，请提供同等说明并记入日志。
- 发生故障或回滚：先在 `state/LOG.md` 记录时间、平台、问题、处理方案，再修改 `state/STATUS.yaml` 与相关文件。
- 引入第三方素材需标注授权；如不可公开，meta 中注明 "internal-only" 并在正文提示读者。

保持以上约定，可让多代理系统稳定地产出符合个人风格、事实准确的 Markdown 博客。
