# Blog Pipeline Dashboard (Template)

更新此文件以摘要当前阶段、分支、任务与守门条件。保持与 `state/STATUS.yaml` 一致，并在表格中写入真实的风格匹配分数、事实核查状态、草稿迭代次数与图片检查结果。

## 当前阶段
- `state/STATUS.yaml` → current_stage: plan（更新时请写入实际阶段与时间戳）

## 任务摘要
| 任务ID | 阶段 | 状态 | 负责人 | 备注 |
|--------|------|------|--------|------|
| style_grounding | plan | todo | stylist | 解析示例文章形成 `state/STYLE_PROFILE.md` |
| material_intake | plan | todo | coordinator | 编写 `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md` |
| research_deepdive | research | todo | researcher | 汇总检索与事实来源 |
| outline_blueprint | outline | blocked | outliner | 需研究完成并锁定关键信息 |
| drafting_loop | draft | blocked | writer | 草稿需通过风格与事实检查 |
| editing_pass | review | blocked | editor | 风格匹配 ≥0.85 且事实核查完成 |
| packaging_release | publish | blocked | publisher | 输出最终 Markdown 与图像素材 |

## 守门条件
- 风格匹配分数 ≥0.85（current: 请写入实际数字）
- 事实核查：pending / complete（current: 请写入状态）
- 草稿迭代次数：0（更新时填写）
- 图文素材检查：pending（确认 `figures/*.png` + `.meta.json`）

> 此文件用于人工状态汇报，可结合脚本自动生成。更新时请同步 `state/LOG.md` 记录风格评估、资料验证、发布打包等关键动作。
