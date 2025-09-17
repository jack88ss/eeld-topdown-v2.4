# 多代理博客写作脚手架

这个仓库由原先的学术论文流水线改造而来，现在专注于**图文并茂的长篇博客**。流程模仿 `/Users/wsy/Downloads/Get 笔记写作助手.srt` 中介绍的多 Agent 协作：风格师锁定语气、调研员搜集事实、策划者搭建段落蓝图、写作者落地草稿、编辑批注并二次打磨，最后由发布者打包 Markdown 与图片素材。

> 推荐通过 `/start-blog`（或等效 orchestrator）串联各子代理，CLI 脚本仅在需要刷新风格画像或执行终检时补充使用。

> 核心产物为 `draft/post.md` 与 `figures/` 下的配图及 `.meta.json` 说明；不再生成 Typst / PDF / Word。

## 目录速览
- `.claude/` / `.codex/`（后续同步）：多代理配置与命令。
- `state/`：进度与事实来源的唯一事实源。
  - `STATUS.yaml` — 工作流状态机（plan → research → outline → draft → review → publish）。
  - `STYLE_PROFILE.md` — 示例文章提炼出的语气画像。
  - `MATERIAL_AUDIT.md` — 用户提供材料与限制清单。
  - `RESEARCH_SUMMARY.md` — 调研摘要与引用矩阵。
  - `POST_OUTLINE.md` / `POST.md` — 大纲与工作稿。
  - `ITERATIONS.md` — 草稿版本与风格分数记录。
  - `LOG.md` — 关键操作、命令与守门条件变更。
- `draft/`：`post.md` 为唯一交付格式，可复制到 Obsidian/Notion。
- `figures/`：`figure_<id>.png` 与同名 `.meta.json` 描述图像位置、版权、段落编号。
- `samples/example-articles/`：内置 13 篇风格样例，供 stylist/ writer 参考。
- `src/blog_pipeline/`：保留的工具脚本（可选），默认优先依赖多代理协作。
- `tools/run_stage.py`：调度/守卫脚本，读取 `state/STATUS.yaml` 判定可执行任务。

## 工作流阶段
1. **Style Grounding**（stylist）
   - 首选复用 `state/STYLE_PROFILE.md` / `.json` 缓存；
   - 仅在用户替换示例文章时才触发重新提炼。
2. **Material Intake**（coordinator）
   - 读取用户指定主题/材料。
   - 更新 `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md`，说明是否需要外部调研。
3. **Research Deepdive**（researcher）
   - 若需扩展资料，执行在线检索或整合用户提供材料。
   - 写入 `state/RESEARCH_SUMMARY.md` 与 `state/SOURCES.md`（引用按 `[@key]` 编号）。
4. **Outline Blueprint**（outliner）
   - 基于风格与事实生成模块化结构，记录在 `state/POST_OUTLINE.md`。
5. **Drafting Loop**（writer）
   - 生成工作稿 `state/POST.md` 并同步对外版 `draft/post.md`。
   - 插入 `![[assets/...]]` 图像占位，确保段落自然、设问频繁。
6. **Editing Pass**（editor）
   - 运行 `python -m src.blog_pipeline.cli check --draft draft/post.md --profile state/STYLE_PROFILE.md`。
   - 产出 `results/style_check.json`（风格分 ≥0.85）与 `results/fact_check.log`。
   - 在 `state/ITERATIONS.md`、`state/LOG.md` 登记。
7. **Packaging Release** (publisher)
   - 确认图片与 `.meta.json` 完整，整理最终 Markdown。
   - 更新 `docs/status.md`、`state/LOG.md`，宣布守门条件达成。

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
- **风格匹配**：`style_match_score ≥ 0.85`，问号占比 ≥ 3%，第二人称频率 ≥ 8 次/篇。
- **事实核查**：`results/fact_check.log` 无缺失；若用户禁止外部调研，需注明“使用提供素材写作”。
- **图像管理**：每张 `figure_<id>.png` 搭配 `.meta.json`（记录段落编号、描述、版权状态）。
- **日志同步**：所有关键命令、评分、打包动作写入 `state/LOG.md` 并在 `state/ITERATIONS.md` 登记版本。

## 只用用户素材 vs. 启动调研
- 若用户说明“不要调研”，`material_intake` 需在 `state/MATERIAL_AUDIT.md` 标记 `覆盖度: full`，`research_deepdive` 可直接引用素材并在 `state/LOG.md` 说明跳过外部检索。
- 若素材不足，则记录缺口，触发 researcher 执行补充检索，注明搜索关键词、时间、来源可信度。

## 与示例文章对齐
样例位于 `/Users/wsy/Dropbox/example-blog-articles/`。建议使用脚本计算：
- 平均段落长度与句长。
- 二人称/设问/比喻关键词频率。
- 图片嵌入位置（寻找 `![[` 模式）。
结果写入 `state/STYLE_PROFILE.md`，供 writer / editor 作为目标值。

## 调度与协同
- `state/STATUS.yaml` 为唯一状态机。任何阶段推进、回滚或并行任务都要更新此文件及 `docs/status.md`。
- `tools/run_stage.py` 在执行前会检查命名守卫：
  - `results/` 中允许 `style_*.json`、`fact_*.log`、`outline_*.md` 等前缀。
  - `figures/` 中 `.png` 必须有同名 `.meta.json`。
- 每次执行命令后在 `state/LOG.md` 追加条目，记录平台（Claude/Codex）、命令、退出码、风格分、事实核查结论。

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
