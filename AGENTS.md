# 代理系统配置指南

## 快速开始

使用 `/start-blog <主题>` 命令启动博客写作流程。系统将自动调度七个专业代理完成任务。

## 代理配置文件

各代理的详细配置位于 `.claude/agents/` 目录：
- `stylist.md` - 风格分析师
- `coordinator.md` - 素材协调员
- `researcher.md` - 调研专家
- `outliner.md` - 结构设计师
- `writer.md` - 内容创作者
- `editor.md` - 质量编辑
- `publisher.md` - 发布管理员
- `orchestrator.md` - 流程调度器

## 状态管理

- **状态机**：`state/STATUS.yaml` 定义任务依赖与守门条件
- **日志追踪**：`state/LOG.md` 记录每个阶段的执行情况
- **迭代记录**：`state/ITERATIONS.md` 保存草稿版本与反馈

## 写作规范

统一规范文档：`state/WRITING_SPEC.md`
- 语气风格要求
- 内容结构模板
- 视觉排版标准
- 质量检查指标

## 注意事项

1. **风格缓存**：`state/STYLE_PROFILE.md` 默认复用，样例更新时刷新
2. **图像管理**：`assets/` 存放图片，`figures/*.meta.json` 记录元数据
3. **引用规范**：`state/SOURCES.md` 统一管理所有外部链接
4. **守门条件**：每个阶段完成前必须满足相应检查点

详细架构说明见 `AGENT_ARCHITECTURE.md`，完整项目规范见 `CLAUDE.md`。
