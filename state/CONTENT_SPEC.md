# 内容与工具规范

## 模块 / 组件
- **src/blog_pipeline/style.py** — 从示例文章抽取语气、句式、设问密度等特征，生成 `style.StyleProfile`。
- **src/blog_pipeline/research.py** — 聚合用户素材与外部检索结果，产出结构化事实摘要，写回 `state/RESEARCH_SUMMARY.md`。
- **src/blog_pipeline/outline.py** — 根据风格与事实生成模块化大纲，更新 `state/POST_OUTLINE.md`。
- **src/blog_pipeline/drafter.py** — 依据大纲与风格生成草稿骨架，写入 `state/POST.md` 与 `draft/post.md`。
- **src/blog_pipeline/editor.py** — 运行风格匹配、设问/人称统计、事实核对；输出 `results/style_check.json`、`results/fact_check.log`。
- **src/blog_pipeline/cli.py** — 命令行入口，协调各阶段任务，可在 `tools/run_stage.py` 调度中被引用。
- **tests/** — 覆盖风格指标计算、素材聚合、草稿检查等核心函数。

## 数据流
1. **风格提炼**：`style.extract_profile(sample_paths)` → 写入 `state/STYLE_PROFILE.md`。
2. **素材审计**：coordinator 整理用户输入 → `state/MATERIAL_AUDIT.md`。
3. **资料整合**：`research.merge(materials, queries)` → 生成 `state/RESEARCH_SUMMARY.md`、更新 `state/SOURCES.md`。
4. **大纲生成**：`outline.build(profile, summary)` → 更新 `state/POST_OUTLINE.md`。
5. **草稿撰写**：`drafter.compose(outline, profile, materials)` → 写入 `state/POST.md`、`draft/post.md`。
6. **编辑校验**：`editor.check(draft_path, profile, sources)` → 输出风格分数、设问/人称计数、引用检查。
7. **发布打包**：`editor.package(draft_path, figures_dir)` → 确认 Markdown、图像与 `.meta.json` 一致，准备发布目录。

## 关键函数
```python
StyleProfile.from_corpus(paths: Sequence[Path]) -> StyleProfile
collect_materials(inputs: MaterialBundle) -> MaterialDigest
build_outline(profile: StyleProfile, summary: ResearchSummary) -> Outline
compose_draft(outline: Outline, profile: StyleProfile, materials: MaterialDigest) -> Draft
measure_style(draft: Draft, profile: StyleProfile) -> StyleReport
merge_sources(reports: Iterable[ResearchFinding]) -> ResearchSummary
render_distribution(report: StyleReport, output: Path) -> None
```
- `StyleProfile.from_corpus`：统计平均句长、问句比例、亲密度词汇、视觉插图频率。
- `measure_style`：返回 `style_match_score`、`question_ratio`、`second_person_ratio` 等指标；低于阈值需触发 `editing_pass`。
- `collect_materials`：支持用户提供的 Markdown、纯文本、URL，自动去重并保留引用。
- `compose_draft`：生成带段落注释的 Markdown，插入图片占位，未实际写作部分保留 `TODO` 标记供 writer 填充。

## 运行命令
- `python -m src.blog_pipeline.cli init-style --corpus /Users/wsy/Dropbox/example-blog-articles --output state/STYLE_PROFILE.md`
- `python -m src.blog_pipeline.cli plan --topic "<主题>" --materials state/MATERIAL_AUDIT.md`
- `python -m src.blog_pipeline.cli draft --outline state/POST_OUTLINE.md --output draft/post.md`
- `python -m src.blog_pipeline.cli check --draft draft/post.md --profile state/STYLE_PROFILE.md`
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
