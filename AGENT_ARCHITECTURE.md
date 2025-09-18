# 多代理博客写作架构

## 总览

系统以 `/start-blog` 为唯一入口，按照 `state/STATUS.yaml` 状态机调度七个专业代理，最终交付 Markdown 博客（`draft/post.md`）与图像资产。

## 代理职责

| 代理 | 职责 | 主要产出 |
|------|------|----------|
| **stylist** | 提炼写作风格 | `state/STYLE_PROFILE.md` |
| **coordinator** | 审计素材与制定计划 | `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md` |
| **researcher** | 收集补充事实资料 | `state/RESEARCH_SUMMARY.md`、`state/SOURCES.md` |
| **outliner** | 设计文章结构 | `state/POST_OUTLINE.md` |
| **writer** | 撰写文章草稿 | `state/POST.md`、`draft/post.md` |
| **editor** | 审核风格与事实 | `state/ITERATIONS.md` 反馈记录 |
| **publisher** | 打包发布检查 | 资产核对、`docs/status.md` 更新 |

## 工作流程

1. **风格基础**：stylist 复用或更新风格缓存
2. **素材准备**：coordinator 整理输入限制
3. **调研深化**：researcher 补充链接事实
4. **结构设计**：outliner 生成段落蓝图
5. **内容创作**：writer 完成初稿
6. **质量审核**：editor 人工审读
7. **发布打包**：publisher 核对资产

## 关键文件

- `state/STATUS.yaml`：状态机与守门条件
- `state/LOG.md`：流程日志与追踪
- `state/WRITING_SPEC.md`：统一写作规范
- `assets/` + `figures/*.meta.json`：图像与元数据

详细规范请参考 `CLAUDE.md`。
