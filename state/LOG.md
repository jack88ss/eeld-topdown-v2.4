| 时间 (UTC) | Actor | Stage | Change | Evidence |
|------------|-------|-------|--------|----------|
| YYYY-MM-DDThh:mm:ssZ | stylist | plan | 完成风格画像，写入 `state/STYLE_PROFILE.md` | state/STYLE_PROFILE.md |
| | coordinator | plan | 记录用户素材、是否允许调研 | state/MATERIAL_AUDIT.md; state/PUBLISH_PLAN.md |
| | researcher | research | 更新调研摘要与引用 | state/RESEARCH_SUMMARY.md; state/SOURCES.md |
| | writer | draft | 产出工作稿，插入图片占位 | state/POST.md; draft/post.md |
| | editor | review | 运行风格/事实校验，记录命令与分数 | results/style_check.json; results/fact_check.log; state/ITERATIONS.md |
| | publisher | publish | 打包最终 Markdown 与图像素材 | draft/post.md; figures/ |

> 更新日志时请追加行，包含执行命令、平台（claude/codex）、退出码、风格分数、事实核查结论等关键细节。
