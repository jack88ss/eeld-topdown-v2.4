# Blog Pipeline Dashboard (Template)

更新此文件以概览阶段、任务状态与守门条件。需与 `state/STATUS.yaml`、`state/LOG.md` 一致，并写明最近更新时间。

## 当前阶段
- `state/STATUS.yaml` → current_stage: plan（更新时请写入实际阶段与时间戳）

## 任务摘要
| 任务ID | 阶段 | 状态 | 负责人 | 备注 |
|--------|------|------|--------|------|
| style_grounding | plan | todo | stylist | 缓存 `state/STYLE_PROFILE.md`，样例变更时更新 |
| material_intake | plan | todo | coordinator | `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md` |
| research_deepdive | research | todo | researcher | 汇总事实、补充 `state/SOURCES.md` |
| outline_blueprint | outline | blocked | outliner | 待调研完成后输出段落蓝图 |
| drafting_loop | draft | blocked | writer | 草稿 (`state/POST.md`/`draft/post.md`) |
| editing_pass | review | blocked | editor | 审阅风格/事实/图像并在日志记录 |
| packaging_release | publish | blocked | publisher | 核对 Markdown + assets + meta |

## 守门条件追踪
- **风格审阅**：stylist / editor 是否在 `state/LOG.md` 留有签字（记录“沿用缓存/刷新样例”“风格反馈”）。
- **事实审阅**：正文引用是否全部链接到 `state/SOURCES.md`；editor 是否在日志记录核查结论。
- **图像检查**：`assets/` 与 `figures/*.meta.json` 是否成对存在；缺项由 publisher 在日志注明补交计划。
- **迭代记录**：`state/ITERATIONS.md` 当前条目数与最新反馈。

> 必须在每次阶段变更后刷新本文件，并附上最近一次 `state/LOG.md` 条目的链接或摘要，方便跨平台追踪。
