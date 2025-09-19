# PPT_API - AI 驱动的演示文稿生成系统

基于大语言模型和联网搜索的智能 PPT 生成项目，能够根据用户输入的主题自动生成专业的 HTML 网页版演示文稿。

## 🚀 核心功能

- **智能主题分析**：输入任意主题，系统自动理解并分析
- **联网信息搜索**：实时获取最新相关信息，确保内容准确性
- **AI 大纲生成**：基于大语言模型生成结构化 PPT 大纲
- **自动配图生成**：集成 ModelScope 文生图服务，为每页生成相关配图
- **HTML 演示文稿**：输出现代化、响应式的 HTML 网页版 PPT
- **专业模板**：内置多种专业演示模板和布局

## 📋 系统架构

```
用户输入主题 → 联网搜索 → AI生成大纲 → 格式化处理 → 配图生成 → HTML渲染 → 完整演示文稿
```

## 🛠️ 技术栈

- **后端框架**：Python + FastAPI
- **AI 模型**：DeepSeek-V3 (大纲生成) + ModelScope Qwen-image (图片生成)
- **前端技术**：HTML5 + TailwindCSS + FontAwesome
- **搜索服务**：联网实时搜索 API
- **数据处理**：ChromaDB (向量数据库)

## 📦 安装部署

### 环境要求

- Python >= 3.11
- Node.js >= 18 (可选，用于前端开发)

### 1. 克隆项目

```bash
git clone https://github.com/neimrai/PPT_API.git
cd PPT_API
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入相关配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# LLM配置
LLM_API_BASE_URL=https://api.deepseek.com
MODEL=deepseek-v3-241226
LLM_API_KEY=your_deepseek_api_key

# ModelScope图片生成
MODELSCOPE_API_KEY=your_modelscope_api_key

# 搜索服务配置
IMAGE_PROVIDER=pexels
IMAGE_URL=https://api.pexels.com/v1/search
IMAGE_API_KEY=your_pexels_api_key

# 其他配置
YAYI_APP_KEY=your_yayi_app_key
YAYI_APP_SECRET_ENV=your_yayi_secret
```

### 4. 运行项目

```bash
python main.py
```

## 🎯 使用方法

### 基本使用

```python
from api.service.generate_presentation_outline import generate_presentation_outline
from api.service.generate_html import generate_slide_html_with_images

# 1. 生成PPT大纲
outline = generate_presentation_outline(
    prompt="人工智能发展趋势",
    slide_number=8,
    language="zh"
)

# 2. 生成HTML演示文稿
html_content = generate_slide_html_with_images("zh", outline)

# 3. 保存到文件
with open("data/presentation.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

### 自定义配置

```python
# 修改main.py中的参数
prompt = "你的演示主题"
n_slides = 10  # 幻灯片数量
language = "zh"  # 语言设置
```

## 📁 项目结构

```
PPT_API/
├── api/
│   ├── prompts/           # AI提示词模板
│   │   ├── HTML-prompt2.md
│   │   └── outline-prompt.md
│   └── service/           # 核心服务模块
│       ├── generate_presentation_outline.py  # 大纲生成
│       ├── generate_html.py                  # HTML生成
│       ├── image_generation_service.py       # 图片生成
│       ├── icon_finder_service.py            # 图标搜索
│       └── web_search_service.py             # 联网搜索
├── data/                  # 输出文件目录
├── my-presentation-app/   # Next.js前端应用(可选)
├── chroma/               # 向量数据库
├── main.py              # 主程序入口
├── .env                 # 环境配置
└── README.md           # 项目说明
```

## 🎨 生成效果

生成的 HTML 演示文稿具有以下特点：

- **现代化设计**：采用 TailwindCSS，界面美观专业
- **响应式布局**：支持不同屏幕尺寸，16:9 宽高比
- **丰富内容**：包含标题、正文、配图、图标等元素
- **交互体验**：支持键盘导航和触摸操作
- **独立运行**：每个幻灯片都是完整的 HTML 文档

## 🔧 高级配置

### 自定义模板

在 `api/prompts/HTML-prompt2.md` 中修改 HTML 模板样式：

```markdown
### 配色方案

- 主色调：#2563eb (蓝色)
- 辅助色：#64748b (灰色)
- 背景色：#f8fafc (浅灰)
```

### 图片生成优化

在 `api/service/image_generation_service.py` 中调整图片生成参数：

```python
image_prompt = f"{title}, professional presentation, clean background, high quality"
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供强大的大语言模型
- [ModelScope](https://modelscope.cn/) - 提供优质的图片生成服务
- [TailwindCSS](https://tailwindcss.com/) - 现代化 CSS 框架
- [FontAwesome](https://fontawesome.com/) - 丰富的图标库

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
