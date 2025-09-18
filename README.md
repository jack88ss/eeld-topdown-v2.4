# 多代理博客写作脚手架

这个仓库从学术论文模板演化而来，如今聚焦**长篇中文博客**。流程依托 `/start-blog` 调用的多代理协作：stylist 锁定语气、researcher 梳理事实、outliner 制定段落、writer 生成正文、editor 审读校对、publisher 打包发布。

> 以代理驱动为先：默认通过 `/start-blog` 或等效 orchestrator 推进工作；Python 脚本仅在必要时作辅助检查。

> 交付物为 Markdown (`draft/post.md`) 与图像资产（`assets/` + `figures/*.meta.json`）；不再生成 Typst / PDF / Word，也不再强制依赖字体文件。

## 目录速览
- `.claude/` / `.codex/`（后续同步）：多代理配置与命令。
- `state/`：进度与事实来源的唯一事实源。
  - `STATUS.yaml` — 工作流状态机（plan → research → outline → draft → review → publish）。
  - `STYLE_PROFILE.md` — 示例文章提炼出的语气画像。
  - `MATERIAL_AUDIT.md` — 用户提供材料与限制清单。
  - `RESEARCH_SUMMARY.md` — 调研摘要与引用矩阵。
  - `POST_OUTLINE.md` / `POST.md` — 大纲与工作稿。
  - `ITERATIONS.md` — 草稿版本与编辑反馈记录。
  - `LOG.md` — 关键操作、命令与守门条件变更。
- `draft/`：`post.md` 为唯一交付格式，可复制到 Obsidian/Notion。
- `assets/`：实际插图或截图；发布前需确保与正文一致。
- `figures/`：存放 `.meta.json` 描述（paragraph、description、source、license、captured_at）。
- `samples/example-articles/`：内置 13 篇风格样例；stylist 默认从此处读取并维护 `state/STYLE_PROFILE.md`。
- `optional-tools/`（可选）：历史脚本与测试集中地，使用前请在 `state/LOG.md` 记录目的与结论。
- `fonts/`：旧流程遗留字体文件，如需用于图片排版可手动引用，默认不强制。
- `tools/run_stage.py`：调度/守卫脚本，读取 `state/STATUS.yaml` 判定可执行任务。

## 工作流阶段
1. **Style Grounding**（stylist）
   - 阅读 `state/STYLE_PROFILE.md` 与 `samples/README.md`；如样例无更新则在日志中记录“沿用缓存”。
   - 若用户替换样例，再以模型/人工总结语气特征，更新 `state/STYLE_PROFILE.md`。
2. **Material Intake**（coordinator）
   - 读取用户指定主题/材料。
   - 更新 `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md`，说明是否需要外部调研。
3. **Research Deepdive**（researcher）
   - 若需扩展资料，执行在线检索或整合用户提供材料。
   - 写入 `state/RESEARCH_SUMMARY.md` 与 `state/SOURCES.md`（使用Markdown链接 `[描述](URL)` 格式）。
4. **Outline Blueprint**（outliner）
   - 基于风格与事实生成模块化结构，记录在 `state/POST_OUTLINE.md`。
5. **Drafting Loop**（writer）
   - 依据大纲在 `state/POST.md` 完成段落草稿，并生成对外稿 `draft/post.md`。
   - 插入 `![[assets/figure_01.png]]` 等图片占位并撰写对应说明。
6. **Editing Pass**（editor）
   - 以人工审读为主：对照 `state/STYLE_PROFILE.md`、事实资料、图片说明，给出修改意见。
   - 如需辅助，可运行 `python -m src.blog_pipeline.cli check ...` 获取提示，再在 `state/LOG.md` 说明是否采纳。
   - 在 `state/ITERATIONS.md` 标记最新一版草稿和关键反馈。
7. **Packaging Release**（publisher）
   - 核对 `assets/` 与 `figures/*.meta.json` 是否成对存在，正文链接是否有效。
   - 更新 `docs/status.md`、`state/LOG.md` 并宣布守门条件达成。

整个流程默认自驱：除非用户明确要求停顿或提供增量材料，代理需按状态机连续推进直至 `packaging_release` 完成。

## 命令示例（当前可用）
```bash
# 1. 启动 orchestrator（推荐）
/start-blog <主题> [--materials ...]

# 2. （可选）若示例文章发生变更，可手动运行缓存脚本
python -m src.blog_pipeline.cli init-style --corpus samples/example-articles --output state/STYLE_PROFILE.md

# 3. （可选）在完成草稿后使用脚本做额外校验
python -m src.blog_pipeline.cli check --draft draft/post.md --profile state/STYLE_PROFILE.md --sources state/SOURCES.md

# 4. 查看 ready 任务（调度守卫）
python tools/run_stage.py
```

> 说明：默认依靠多代理阅读样例和草稿完成风格提炼与事实审校；以上脚本仅作为必要时的辅助工具。

## 守门条件
- **风格**：stylist/ editor 均在 `state/LOG.md` 签字确认语气一致，并列出核心改动建议。
- **事实**：引用段落需附带行文链接或脚注，并在 `state/SOURCES.md` 列出对应来源；editor 在日志中说明核查结论。
- **图像**：`assets/` 与 `figures/*.meta.json` 成对存在，meta 包含来源与许可；publisher 在 `state/LOG.md` 登记检查结果。
- **日志**：每次阶段完成需追加 `state/LOG.md` 条目，`state/ITERATIONS.md` 记录草稿版本与反馈。

## 只用用户素材 vs. 启动调研
- 若用户说明“不要调研”，`material_intake` 需在 `state/MATERIAL_AUDIT.md` 标记 `覆盖度: full`，`research_deepdive` 可直接引用素材并在 `state/LOG.md` 说明跳过外部检索。
- 若素材不足，则记录缺口，触发 researcher 执行补充检索，注明搜索关键词、时间、来源可信度。

## 与示例文章对齐
- 样例集中存放在 `samples/example-articles/`，简要摘要见 `samples/README.md`。
- 每次写作前，stylist/ writer 应阅读相近主题样例，提炼要点并更新 `state/STYLE_PROFILE.md` 或 `state/VOICE_AND_STRUCTURE.md`。
- 若引入新样例，请保留原文件、补写摘要，并在 `state/LOG.md` 记录更新原因。

## 调度与协同
- `state/STATUS.yaml` 描述阶段与任务依赖；推进、回滚或并行任务时需同步 `docs/status.md` 与 `state/LOG.md`。
- `/start-blog` 为推荐入口：协调器读取 state 文档、触发子代理并等待守门条件完成后汇报。
- `tools/run_stage.py` 仅用于列出 ready 任务或快速检查资产状态，不再强制校验 JSON 报告。
- 关键操作需写入 `state/LOG.md`（含时间戳、平台、负责人、要点），`state/ITERATIONS.md` 记录草稿版本、反馈与下一步。

## 下一步开发建议
1. 在 `src/blog_pipeline/` 中实现实际分析与写作模块，并为关键函数补充单元测试。
2. 提供自动化脚本，根据 `state/STATUS.yaml` 的 `command` 字段调用相应 CLI。
3. 构建风格学习缓存：对样例文章进行向量化，减少每次提取开销。
4. 集成图像检索/生成模块，自动填充缺失配图并更新 `.meta.json`。

欢迎继续扩展，使其成为“主题→Markdown 博客”的端到端写作利器。
## 样例文章缓存
- 样例文本位于 `samples/example-articles/`，作为个人风格基准。
- `state/STYLE_PROFILE.md` 保存最近一次的人工总结；stylist 默认沿用该缓存，仅在样例更新时重写。
- 若用户提供额外范例，可先放入该目录再触发 `/start-blog`，或直接在 `state/STYLE_PROFILE.md` 追加备注。
