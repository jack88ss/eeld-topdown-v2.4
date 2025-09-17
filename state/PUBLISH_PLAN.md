# 发布计划 (Blog Workflow)

> 由 coordinator 撰写并经 editor 审视后生效。计划一旦更新需同步 `state/STATUS.yaml` 与 `docs/status.md`，并在 `state/LOG.md` 添加 "Plan Sync" 记录。

## 核心命题
- **主题阐述**：<一句话描述博客要解决的读者困扰>
- **目标读者**：<例如“习惯使用多工具的知识工作者”>
- **成功判据**：读者能获得 <行动/理解>，并愿意在结尾反馈或尝试建议。

## 约束与里程碑
| 里程碑 | 日期 (UTC) | 描述 | 守门条件 |
|--------|-----------|------|----------|
| G1 | 2025-09-18 | 完成 `state/STYLE_PROFILE.md` 与 `state/MATERIAL_AUDIT.md` | 风格要素归纳完备 |
| G2 | 2025-09-20 | 完成调研、引用梳理与 `state/RESEARCH_SUMMARY.md` | 事实来源≥8 条，引用格式一致 |
| G3 | 2025-09-22 | 输出 `state/POST_OUTLINE.md` 与首版草稿 `state/POST.md` | 风格分数≥0.80 |
| G4 | 2025-09-24 | 完成编辑、事实核查、发布包 | 风格分数≥0.85，事实核查完成 |

## 任务分工
- **stylist**：抽取示例文章语言特征，生成 `state/STYLE_PROFILE.md`。
- **coordinator**：整理素材审核表、维护状态、触发调度。
- **researcher**：执行外部检索或整理用户提供材料，输出事实摘要。
- **outliner**：设计段落与模块顺序。
- **writer**：撰写草稿、整合引用与图片。
- **editor**：负责风格评估、事实核查与语气修正。
- **publisher**：确认图片元数据、打包最终 Markdown。

## 风险与缓解
- **风格偏差**：草稿未达到示例文章的语气。→ 安排额外风格比对（`python -m src.blog_pipeline.cli check`），并在 `state/ITERATIONS.md` 记录分数。
- **资料不足**：用户未提供足够素材。→ researcher 提前在 `state/MATERIAL_AUDIT.md` 标注缺口，并触发补充检索。
- **图像版权不明**：新增素材来源不明。→ publisher 在 `.meta.json` 标注版权信息，必要时更换图片。

## 输出节奏
1. **Day 1**：完成风格提炼与素材审计。
2. **Day 2**：完成外部调研与引用登记。
3. **Day 3**：产出结构化草稿，编辑通过风格检查。
4. **Day 4**：完成发布包与归档，并更新 `docs/status.md`。

## 后续动作
- 制定更新计划：<例如“1 周后根据读者反馈更新行动建议段落”>
- 待办列表：<列出潜在的衍生选题或素材>
