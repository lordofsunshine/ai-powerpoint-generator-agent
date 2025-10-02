# 📺 AI PowerPoint Presentation Generator

Command-line utility for creating presentations using artificial intelligence based on io.net API service.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-0.0.3-green.svg)

## 🌐 Language / Язык

| Language | Readme |
|----------|--------|
| 🇷🇺 **Русский** | [README.md](README.md) |
| 🇺🇸 **English** | [README_EN.md](README_EN.md) |

---

<img alt="Banner" width="600" src="https://i.postimg.cc/28R1B8fD/image.png">
<img alt="Banner" width="600" src="https://i.postimg.cc/jdbjSgy3/image.png">

## 🆕 What's New?

### Major Changes:
- **Migration to io.net API** - Replaced G4F with powerful io.net API service providing access to 17+ modern AI models
- **Real-time Web Search** - Slides now contain up-to-date information thanks to search engine integration
- **Current Date Awareness** - AI knows the current date, crucial for relevant content generation
- **Smart Text Wrapping** - Automatic formatting of long text on slides
- **Extended Color Palette** - 16+ new color schemes with automatic selection based on keywords
- **Complete Localization** - Full interface translation to Russian and English

### New Features:
- **Title and Conclusion Slides** - Automatic creation of intro and summary slides
- **Enhanced Settings Menu** - Configure interface language, AI model, web search
- **Developer Mode** - View AI "thinking" process during generation
- **Project Integrity Checks** - Validation of all libraries and files at startup
- **Improved AI Prompts** - Redesigned prompts for higher quality content
- **Strict Validation** - Generation stops on critical errors
- **Auto Directory Creation** - Output folder created automatically

## 🔧 io.net API Key Setup

### Getting API Key:

1. **Register on io.net:**
   - Go to [io.net](https://io.net/)
   - Create account or sign in to existing one

2. **Obtain API Key:**
   - In your dashboard, find "API Keys" or "Developers" section
   - Create new API key
   - Copy the generated key

3. **Setup in Program:**
   - On first run, program will automatically request API key
   - Paste copied key and press Enter
   - Key will be saved in `config/api_key.txt` file

### Available AI Models:

Program supports 17 modern AI models through io.net:

**Top Recommended Models:**
- `deepseek-ai/DeepSeek-R1-0528` (default) - Latest DeepSeek model with best quality
- `meta-llama/Llama-3.3-70B-Instruct` - Proven Meta model with excellent balance
- `Qwen3-235B-A22B-Thinking-2507` - Powerful Qwen model with "thinking" capability
- `mistralai/Mistral-Large-Instruct-2411` - Large Mistral model for complex tasks

**Fast Models:**
- `Mistral-Nemo-Instruct-2407` - Fast and efficient model
- `gpt-oss-20b` - Lightweight GPT version
- `mistralai/Magistral-Small-2506` - Compact Mistral model

**Specialized Models:**
- `Intel/Qwen3-Coder-480B-A3B-Instruct-int4-mixed-ar` - For code generation
- `Qwen/Qwen2.5-VL-32B-Instruct` - With image support
- `meta-llama/Llama-3.2-90B-Vision-Instruct` - Meta Vision model
- `BAAI/bge-multilingual-gemma2` - Multilingual model

**Complete List of Available Models:**
1. DeepSeek R1 - `deepseek-ai/DeepSeek-R1-0528`
2. Swiss AI Apertus - `Apertus-70B-Instruct-2509`
3. Meta Llama 4 Maverick - `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8`
4. OpenAI GPT OSS 120B - `gpt-oss-120b`
5. Qwen3 Coder - `Intel/Qwen3-Coder-480B-A35B-Instruct-int4-mixed-ar`
6. Qwen3 Next - `Qwen3-Next-80B-A3B-Instruct`
7. OpenAI GPT OSS 20B - `gpt-oss-20b`
8. Qwen3 Thinking - `Qwen3-235B-A22B-Thinking-2507`
9. Mistral Nemo - `Mistral-Nemo-Instruct-2407`
10. Mistral Magistral Small - `mistralai/Magistral-Small-2506`
11. Mistral Devstral Small - `mistralai/Devstral-Small-2505`
12. LLM360 K2-Think - `K2-Think`
13. Meta Llama 3.3 - `meta-llama/Llama-3.3-70B-Instruct`
14. Mistral Large - `mistralai/Mistral-Large-Instruct-2411`
15. Qwen2.5 Vision-Language - `Qwen/Qwen2.5-VL-32B-Instruct`
16. Meta Llama 3.2 Vision - `meta-llama/Llama-3.2-90B-Vision-Instruct`
17. BAAI BGE Multilingual - `BAAI/bge-multilingual-gemma2`

### Switching AI Model:

1. In main menu select "⚙ General Settings" (option 3)
2. Choose "AI Settings" (option 3)
3. Select desired model from list
4. Settings save automatically

## ✨ Features

- [x] **Beautiful CLI Interface** with Windows CMD support and colored output
- [x] **PPTX File Creation** with professional design and decorations
- [x] **AI-Agent Correction** of presentations through prompts with progress bar
- [x] **Automatic Slide Decorations** (shapes, colors, accents)
- [x] **SQLite3 Database** for storing presentations and settings
- [x] **Complete Localization** in Russian and English
- [x] **Presentation Management** with automatic opening of ready files
- [x] **Smart Formatting** of lists, two-column slides, tables
- [x] **Web Search** for current information (DuckDuckGo)
- [x] **17+ AI Models** available through io.net API
- [x] **Project Integrity Checks** on every startup

## 🚀 Installation

### Requirements:
- Python 3.8+
- Windows/Linux/macOS
- Internet connection
- io.net API key

### Installation Steps:

1. **Clone Repository:**
```bash
git clone https://github.com/lordofsunshine/ai-powerpoint-generator-agent.git
cd ai-powerpoint-generator-agent
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run Program:**
```bash
python run.py
```

4. **Initial Setup:**
   - On first run, enter io.net API key
   - Choose interface language (Russian/English)
   - Configure AI model in settings menu (optional)

## 🎨 Decorative Elements

Each slide automatically receives professional decorations:
- **Corner Accents** - colored elements in slide corners
- **Side Shapes** - geometric shapes for visual variety
- **Background Elements** - subtle colored blocks for structuring
- **Color Accents** - automatic highlighting of important elements
- **Minimalist Lines** - thin decorative elements
- **Dynamic Color Schemes** - palette selection based on presentation theme

*Decorations and their placement are determined by AI based on slide content.*

## ⚙️ Program Settings

### Main Presentation Parameters:
- **Title** - Main presentation theme
- **Content Language** - Russian or English
- **Number of Sections** - Main sections (default: 1)
- **Slides per Section** - Number of slides in each section (default: 4)
- **Web Search** - Enable/disable current information search

### Interface Settings:
- **Interface Language** - Russian/English
- **Developer Mode** - Show AI generation process
- **Auto-open** - Automatic opening of ready presentations

### AI Settings:
- **AI Model** - Choose from 17+ available models
- **Generation Temperature** - Configure AI creativity
- **Max Response Length** - Limit content size

## 🔍 Web Search

Program can search for current information on the internet to create relevant slides:

### Web Search Settings:
- **Search Engine**: DuckDuckGo (default)
- **Results Count**: 1-10 (default: 5)
- **Search Region**: Russia/USA/Global
- **Content Filtering**: Automatic removal of irrelevant information

### How It Works:
1. AI analyzes slide topic
2. Forms search queries
3. Searches for current information online
4. Integrates found data into slide content
5. Checks relevance and information quality

## 🛠️ Troubleshooting

### Common Issues:

**API Key Error:**
- Check io.net key correctness
- Ensure internet connection
- Check API limits on io.net

**Library Issues:**
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Update Python to version 3.8+
- Check project integrity through program menu

**Generation Errors:**
- Try different AI model in settings
- Disable web search with unstable internet
- Reduce slide count for testing

## 📝 License

This project is distributed under MIT License. See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions to the project! If you want to help:

1. Fork the repository
2. Create branch for new feature
3. Make changes
4. Create Pull Request

## 📞 Support

If you have questions or problems:
- Create Issue on GitHub
- Describe problem in detail
- Attach error logs (if any)

## 🌟 About Project Future

This project represents a powerful tool for automatic generation of professional presentations. Unlike commercial services, there are no limits on slide count, watermarks, or paid subscriptions.

**Development Plans:**
- Integration with more AI providers
- Extended templates and designs
- Adding animations and transitions
- Support for images and diagrams
- Export to other formats (PDF, HTML)

The project actively develops thanks to the user community. Your support and feedback help make it better!

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=lordofsunshine/ai-powerpoint-generator-agent&type=Date)](https://www.star-history.com/#lordofsunshine/ai-powerpoint-generator-agent&Date)