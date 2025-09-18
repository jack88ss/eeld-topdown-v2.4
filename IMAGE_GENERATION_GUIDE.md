# 图像生成与管理指南

## 问题诊断

当前系统存在以下图像相关问题：
1. **图片文件缺失**：`assets/` 目录中无实际图片文件，仅有占位符引用
2. **元数据不完整**：`figures/*.meta.json` 文件虽存在但多为TODO状态
3. **生成机制缺失**：系统未集成自动图像生成或获取工具

## 图像处理策略

### 方案A：AI图像生成（推荐）

使用AI工具自动生成所需图片：

1. **概念图/流程图**（.svg格式）
   - 使用Mermaid或PlantUML生成
   - 通过代码定义图表结构
   - 自动导出为SVG格式

2. **界面截图**（.png格式）
   - 使用Puppeteer或Playwright自动截图
   - 访问目标网站并捕获特定区域
   - 保存为高质量PNG

3. **示意图/配图**（.jpg/.png格式）
   - 集成DALL-E或Stable Diffusion API
   - 根据描述生成相关配图
   - 或使用Unsplash/Pexels API获取免费图片

### 方案B：手动图片准备

1. **预先准备图片库**
   - 在 `samples/images/` 建立常用图片库
   - 按主题分类（技术/工具/概念等）
   - writer代理根据需要选择合适图片

2. **占位符转换系统**
   - 保持占位符机制
   - 发布前批量替换为实际图片
   - 使用映射表管理占位符与实际文件关系

## 实施步骤

### 1. 增强Writer代理

```python
# 在writer代理中添加图像生成逻辑
def generate_image_for_paragraph(paragraph_num, description):
    """根据段落需求生成或获取图片"""
    if is_diagram(description):
        return generate_mermaid_diagram(description)
    elif is_screenshot(description):
        return capture_screenshot(get_url(description))
    else:
        return fetch_stock_image(description)
```

### 2. 创建图像生成工具

在 `tools/` 目录下创建图像工具：

```bash
tools/
├── image_generator.py    # 图像生成主逻辑
├── mermaid_renderer.py    # Mermaid图表渲染
├── screenshot_tool.py     # 网页截图工具
└── stock_fetcher.py      # 免费图库获取
```

### 3. 更新Publisher验证

publisher代理需要增强验证逻辑：
- 检查所有占位符是否有对应实际文件
- 验证图片文件格式和大小
- 确认meta.json中的license信息

## 配置示例

在 `.claude/agents/writer.md` 中添加：

```yaml
image_generation:
  enabled: true
  strategies:
    - type: mermaid
      for: [flowchart, diagram, process]
    - type: screenshot
      for: [interface, demo, example]
    - type: stock
      for: [atmosphere, concept, metaphor]
  fallback: placeholder
```

## 元数据模板

完整的 `figures/figure_01.meta.json` 示例：

```json
{
  "filename": "figure_01.jpg",
  "paragraph": 1,
  "description": "开发者深夜编程的氛围图",
  "source": "generated_by_ai",
  "license": "CC0",
  "captured_at": "2025-09-18T12:00:00Z",
  "generation_prompt": "Developer working late at night with multiple monitors showing code",
  "alt_text": "开发者在深夜面对多个显示器编程的场景"
}
```

## 快速修复方案

立即可用的最小化方案：

1. **创建占位符图片**
   ```bash
   # 生成简单的占位符图片
   for i in {01..11}; do
     convert -size 800x400 xc:gray -pointsize 48 \
       -draw "text 350,200 'Figure $i'" \
       assets/figure_$i.png
   done
   ```

2. **更新引用格式**
   - 将 `![[assets/figure_01.jpg]]` 改为标准Markdown：`![图1说明](assets/figure_01.jpg)`

3. **批量更新meta.json**
   - 将所有TODO替换为实际描述
   - 标注source为"placeholder"
   - 设置license为"pending"

## 长期改进建议

1. **集成图像生成API**
   - OpenAI DALL-E 3
   - Stability AI
   - Midjourney API

2. **建立图片资源池**
   - 常用技术图标
   - 概念示意图模板
   - 界面截图库

3. **自动化工作流**
   - 文章完成后自动触发图像生成
   - 基于描述智能选择生成策略
   - 自动优化图片大小和格式

## 注意事项

- **版权合规**：确保所有图片有明确授权
- **性能优化**：控制图片大小，建议单张不超过500KB
- **可访问性**：为所有图片提供alt文本
- **一致性**：保持图片风格统一
