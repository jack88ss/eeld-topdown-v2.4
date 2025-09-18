# 内容与工具规范

## 核心流程
1. **风格提炼（stylist）**：默认沿用 `state/STYLE_PROFILE.md`；仅在 `samples/example-articles/` 更新时重新总结，并记录在 `state/LOG.md`。
2. **素材审计（coordinator）**：将主题、素材路径、禁忌话题、调研权限记录于 `state/MATERIAL_AUDIT.md`，并在 `state/PUBLISH_PLAN.md` 制定里程碑。
3. **资料整合（researcher）**：补充事实、链接与数据，更新 `state/RESEARCH_SUMMARY.md`、`state/SOURCES.md`（使用普通 Markdown 链接）。
4. **大纲生成（outliner）**：在 `state/POST_OUTLINE.md` 列出模块、目标、引用/图片需求。
5. **写作（writer）**：依据大纲在 `state/POST.md` 撰写草稿，输出 `draft/post.md`，嵌入 `![[assets/figure_01.png]]` 等图像占位。
6. **编辑（editor）**：人工审读语气、事实、图像；在 `state/ITERATIONS.md`、`state/LOG.md` 记录反馈，必要时注明脚本辅助结论。
7. **发布（publisher）**：核对 Markdown、`assets/`、`figures/*.meta.json`，确认链接与许可，更新 `docs/status.md` 并宣布 ready。

## 资产管理
- 图片须存放于 `assets/`，并创建对应的 `figures/figure_##.meta.json`（字段：`paragraph`、`description`、`source`、`license`、`captured_at`）。
- 未完成的图片任务在 `state/POST.md` 标记 TODO，并在 `state/LOG.md` 指定负责人与截止时间。
- 发布前由 publisher 抽查 `assets/` 预览，确保无乱码或敏感信息泄露。

## 引用与链接
- 正文使用行内链接或脚注；示例：`[效率报告](https://example.com)`。
- `state/SOURCES.md` 采用 Markdown 列表：`- 标题 — 来源；日期；链接（说明）`。
- 对内部或付费资源，在正文与 `SOURCES.md` 标注“仅内部引用”或权限说明。

## 可选工具
- 历史脚本位于 `optional-tools/src/blog_pipeline/`，可辅助提炼风格或生成提示；运行前需在 `state/LOG.md` 记录命令与目的。
- 脚本输出仅作参考，最终结论以人工审阅为准。
- 如需测试或依赖，请在 `optional-tools/README.md` 补充说明，并确保不会影响默认流程。

## 守门条件参考
- Stylist 与 editor 在 `state/LOG.md` 确认当前稿件满足语气与事实要求。
- `state/SOURCES.md` 覆盖正文引用的所有链接，并验证可访问性。
- `assets/` 与 `figures/*.meta.json` 成对存在；缺项需在日志列出补救计划。
- `state/ITERATIONS.md` 至少包含“草稿初版”“编辑反馈”“终稿确认”三条记录。

## 协作提示
- 样例与风格缓存的更新要在 `samples/README.md`、`state/STYLE_PROFILE.md` 同步，并在日志注明原因。
- 若某阶段被阻塞（例如素材不足、图像缺失），在 `state/STATUS.yaml` 将任务标记为 `blocked` 并描述后续动作。
- 发布后可在日志记录读者反馈或待改进点，为下一轮写作提供输入。
