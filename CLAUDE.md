# 项目章程（博客写作）

- **目标**：从主题或素材出发，生成贴合原作者语气的中文长篇博客；唯一交付格式为 `draft/post.md`（含 `![[assets/...]]` 图像占位）。
- **多代理分工**：
  1. `stylist` — 分析示例文章，输出 `state/STYLE_PROFILE.md`。
  2. `coordinator` — 对齐用户需求与限制，更新 `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md`。
  3. `researcher` — 整理或补充事实，维护 `state/RESEARCH_SUMMARY.md` 与 `state/SOURCES.md`。
  4. `outliner` — 生成结构化大纲 `state/POST_OUTLINE.md`。
  5. `writer` — 撰写 `state/POST.md`、`draft/post.md`，确保图像与引用放置正确。
  6. `editor` — 执行风格匹配、事实核对，产出 `results/style_check.json`、`results/fact_check.log` 并在 `state/ITERATIONS.md` 登记。
  7. `publisher` — 打包 Markdown 与图像素材，更新 `docs/status.md`、`state/LOG.md`。
- **状态机**：`state/STATUS.yaml` 管理阶段（plan → research → outline → draft → review → publish），守门条件包括风格分 ≥0.85、事实核查完成、图片元数据齐全。
- **事实源**：`state/` 目录内文档为唯一真相。所有代理修改时必须追加记录，不得覆盖历史。
- **调研策略**：
  - 若用户材料充足，可跳过外部检索，在 `state/MATERIAL_AUDIT.md` 标记并在 `state/LOG.md` 说明。
  - 若需要扩展，优先使用高质量来源（官方博客、权威媒体、学术文章），在 `state/SOURCES.md` 记录引用并在正文使用 `[@key]`。
- **风格守门条件**：
  - `style_match_score ≥ 0.85`
  - 问号占比 ≥ 3%
  - 第二人称频率 ≥ 8 次/篇
  - 平均句长 ≤ 24 字
- **事实核查**：每个可验证事实需标注来源。`results/fact_check.log` 应列出段落编号、事实摘要、对应 `[@key]` 或素材链接。缺失时不得进入发布阶段。
- **图像策略**：
  - 每张图片需有 `.meta.json` 说明段落位置、用途、许可证。
  - 发布前使用本地预览确认中文无乱码。
  - 若引用用户提供图片，需在 `.meta.json` 中标记“user-supplied”。
- **日志要求**：
  - 每个阶段完成后向 `state/LOG.md` 追加条目，包含时间戳、负责人、执行命令、退出码、输出文件。
  - `state/ITERATIONS.md` 记录草稿版本演进与风格/事实指标。
- **禁止事项**：
  - 不得生成 Typst/PDF/Word。
  - 不得虚构来源或引用。
  - 不得擅自修改用户素材路径或覆盖原文件。
- **交付物**：
  - `state/STYLE_PROFILE.md`
  - `state/MATERIAL_AUDIT.md`
  - `state/PUBLISH_PLAN.md`
  - `state/RESEARCH_SUMMARY.md`
  - `state/POST_OUTLINE.md`
  - `state/POST.md`
  - `state/ITERATIONS.md`
  - `draft/post.md`
  - `figures/figure_<id>.png` + `.meta.json`
  - `results/style_check.json`
  - `results/fact_check.log`
  - `state/LOG.md`
- **阶段闸口**：
  - G1：`STYLE_PROFILE.md` + `MATERIAL_AUDIT.md` 完成并在 `state/LOG.md` 记录。
  - G2：`RESEARCH_SUMMARY.md`、`SOURCES.md` 完成，引用数 ≥8（或记录“仅用提供素材”）。
  - G3：`POST_OUTLINE.md`、`POST.md` 初稿完成，风格分 ≥0.80。
  - G4：`results/style_check.json` ≥0.85、`results/fact_check.log` 完成，`figures/*.meta.json` 完备。
  - Publish：`draft/post.md` 最终版上传，`docs/status.md` 更新，`state/STATUS.yaml` 设为 `publish` 或 `done`。

保持上述规则，确保每篇文章都兼具个人风格、事实扎实、素材齐全。
