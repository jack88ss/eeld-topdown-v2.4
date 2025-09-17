# 内容与工具规范

## 模块 / 组件
- **src/blog_pipeline/style.py** — 从示例文章抽取语气、句式、设问密度等特征，生成 `StyleProfile` 并写入 `state/STYLE_PROFILE.md` + JSON 缓存。
- **src/blog_pipeline/check.py** — 运行风格匹配、设问/人称统计、图像密度与引用检查；输出 `results/style_check.json`、`results/fact_check.log`。
- **src/blog_pipeline/text_utils.py** — 共有的段落/句子分割与指标计算函数。
- **src/blog_pipeline/cli.py** — 暴露 `init-style`、`check` 子命令，供 orchestrator 或手动触发。
- **未来模块占位**：`research.py`、`outline.py`、`drafter.py`、`editor.py` 可按需要逐步补齐，用于自动化调研、大纲与草稿。
- **tests/** — 覆盖现有模块（`style`、`check`、`text_utils`）的核心函数，新增模块时同步补测。

## 数据流
1. **风格提炼**：`style.extract_profile(sample_paths)` → 写入 `state/STYLE_PROFILE.md`。
2. **素材审计**：coordinator 手动整理用户输入 → `state/MATERIAL_AUDIT.md`（未来可由脚本补充）。
3. **资料整合**：researcher 手动或脚本化更新 `state/RESEARCH_SUMMARY.md`、`state/SOURCES.md`。
4. **大纲生成**：outliner 在 `state/POST_OUTLINE.md` 维护模块顺序与要点。
5. **草稿撰写**：writer 在 `state/POST.md`、`draft/post.md` 完成正文与图像占位。
6. **编辑校验**：`check.check_draft` + `check.fact_check` 组合生成风格与事实报告。
7. **发布打包**：publisher 对 `draft/post.md`、`figures/`、`.meta.json` 做最终确认。

## 关键函数
```python
StyleProfile.from_corpus(paths: Sequence[Path]) -> StyleProfile
check_draft(draft_path: Path, profile_path: Path) -> StyleCheckReport
fact_check(draft_path: Path, sources_path: Path) -> tuple[str, list[str]]
# 下列函数为后续扩展参考
# collect_materials(...)
# build_outline(...)
# compose_draft(...)
```
- `StyleProfile.from_corpus`：统计平均句长、问句比例、亲密度词汇、视觉插图频率。
- `check_draft`：产出 `style_match_score`、`question_ratio`、`second_person_ratio`、配图密度等指标。
- `fact_check`：解析 Markdown 中的 `[@key]` 与外链，生成可追溯的事实核查日志。

## 运行命令
- `python -m src.blog_pipeline.cli init-style --corpus /Users/wsy/Dropbox/example-blog-articles --output state/STYLE_PROFILE.md`
- `python -m src.blog_pipeline.cli check --draft draft/post.md --profile state/STYLE_PROFILE.md --sources state/SOURCES.md`
- 调度脚本：`python tools/run_stage.py --stage draft --run`（结合 manifest 的命令字段）。

## 验证标准
- `results/style_check.json`：包含 `style_match_score`（≥0.85）、`question_ratio`（≥0.03）、`second_person_ratio`（≥0.08）。
- `results/fact_check.log`：列出每个事实句对应的来源标识；缺失时编辑需补充或删减。
- 所有图像需在 `figures/` 下配套 `.meta.json`，描述出处、段落位置（例如 `P3`）。
- 输出目录 `draft/post.md` 与 `figures/` 内容一致；若发布到 Obsidian/Notion，需保留 `![[assets/...]]` 嵌入格式。

## 协作与交付
- writer 更新草稿后必须运行 `python -m src.blog_pipeline.cli check` 并将输出写入 `state/ITERATIONS.md`。
- editor 在 `state/LOG.md` 中记录风格评分、事实核查步骤与命令退出码。
- publisher 负责将 `draft/post.md` 与图像素材打包，并在 `.meta.json` 中更新最终发布时间。
