| id | 时间 (UTC) | 涉及任务 | 变更摘要 | 风格分数 | 事实核查 | 产物 |
|----|------------|----------|----------|----------|----------|------|
| draft_v1 | YYYY-MM-DDThh:mm:ssZ | drafting_loop | <首次成稿> | <0.x> | pending | draft/post.md |
| draft_v1_edit | | editing_pass | <编辑修改说明> | <0.x> | <complete/pending> | draft/post.md; results/style_check.json; results/fact_check.log |
| draft_final | | packaging_release | <最终发布包> | ≥0.85 | complete | draft/post.md; figures/ |

> 在每次迭代后更新本表，并于 `state/LOG.md` 写入对应记录（含负责人、验证命令、退出码）。风格分数取自 `results/style_check.json` 或等效工具，事实核查列需链接到检查条目。
