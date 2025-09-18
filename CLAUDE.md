# 项目章程（博客写作）

- **目标**：围绕用户主题生成贴合个人语气的中文博客；交付物为 `draft/post.md` + 图像资产（`assets/` 与 `figures/*.meta.json`）。
- **多代理分工**：
  1. `stylist` — 复用或更新 `state/STYLE_PROFILE.md`，总结语气与结构要点。
  2. `coordinator` — 梳理输入材料与限制，更新 `state/MATERIAL_AUDIT.md`、`state/PUBLISH_PLAN.md`。
  3. `researcher` — 汇总事实并记录链接，维护 `state/RESEARCH_SUMMARY.md`、`state/SOURCES.md`（普通 Markdown 列表）。
  4. `outliner` — 生成段落蓝图 `state/POST_OUTLINE.md`，指出图像与引用需求。
  5. `writer` — 在 `state/POST.md`、`draft/post.md` 完成草稿，插入 `![[assets/...]]`，保持设问与亲切语气。
  6. `editor` — 人工审读风格/事实/图像，并在 `state/ITERATIONS.md`、`state/LOG.md` 登记反馈；可选用脚本辅助但必须说明结论。
  7. `publisher` — 核对 Markdown 与资产、更新 `docs/status.md`，在 `state/LOG.md` 宣布 ready。
- **状态机**：`state/STATUS.yaml` 维护阶段与守门条件；`/start-blog` 负责解析并调度。
- **事实源**：`state/` 与 `samples/` 目录构成单一事实来源，所有修改须追加而非覆盖历史。
- **核心规范**：`state/WRITING_SPEC.md` 统一定义语气风格、内容结构、视觉排版与质量指标。
- **内心独角戏系统**：每个代理必须在 `state/LOG.md` 中记录剧本式的工作过程，包括登场介绍、观察输入、内心独白、决策过程、执行动作五幕（详见 `AGENT_MONOLOGUE_SYSTEM.md`）。
- **调研策略**：
  - 若仅使用用户素材，在 `state/MATERIAL_AUDIT.md` 标注"外部调研：关闭"，并在日志说明原因。
  - 需要扩展时，优先官方或权威媒体；在正文中使用行内链接，并在 `state/SOURCES.md` 记录标题、来源、日期、URL。
- **长度要求**：文章正文必须达到3000字以上（不含标题、图片说明），通过深入案例分析、多角度探讨、扩展思考等方式充实内容。
- **风格守门条件**：
  - Stylist 与 editor 均在 `state/LOG.md` 确认语气符合缓存要点。
  - 段落平均长度 ≈ 80–150 字；10–15个设问均匀分布；第二人称至少20次。
- **事实守门条件**：
  - 每个重要论断需提供可访问链接或脚注；editor 在 `state/LOG.md` 记录核查结论。
- **图像策略**：
  - 用户提供图片时，根据内容相关性智能放置，保存为 `assets/user_provided_##.ext`。
  - 复杂概念使用Mermaid图表拆解（流程图、时序图、架构图等）。
  - 数据可视化：少量用表格，大量用Mermaid图表。
  - 仅在确实需要时使用占位符，避免大量空白图片。
  - 取消强制的.meta.json要求，图表直接嵌入Markdown。
- **日志要求**：
  - 采用剧本式记录（参考 `state/LOG_TEMPLATE.md`），每个代理需完整记录五幕独角戏。
  - 记录应真实反映思考过程，包括困惑、失败尝试、决策理由（200-500字/代理）。
  - `state/ITERATIONS.md` 记录草稿版本、关键反馈、待办事项。
  - 多代理协作时记录对话，展现信息流转过程。
- **禁止事项**：
  - 不得生成 Typst/PDF/Word。
  - 不得虚构引用或隐藏素材来源。
  - 不得覆盖他人日志或删除历史记录。

## 守门条件示例
- G1（plan）：`STYLE_PROFILE.md`、`MATERIAL_AUDIT.md` 更新并在日志记录“沿用/刷新”决定。
- G2（research）：`RESEARCH_SUMMARY.md`、`SOURCES.md` 完成，注明资料缺口或确认仅用用户素材。
- G3（draft）：`POST_OUTLINE.md`、`POST.md` 初稿完成，editor 提供首轮反馈并登记于 `ITERATIONS.md`。
- G4（review）：editor 在 `state/LOG.md` 签字确认风格/事实无阻塞；图片 TODO 已解决。
- Publish：publisher 检查 `assets/` 与 `.meta.json` 成对存在，`docs/status.md` 更新，`STATUS.yaml` 设为 `publish` 或 `done`。

遵循以上约束，可确保每篇文章在保持个人风格的同时，具备可靠的事实支撑与图文一致性。
