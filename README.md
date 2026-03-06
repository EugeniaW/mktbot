 Deep Research Bot

AI-powered marketing research bot for Telegram. Generates structured Markdown reports from web search.

 Features

-  `/research <topic>` - Deep research with structured Markdown reports
-  `/quick <topic>` - Fast search summaries  
-   Powered by Tavily AI Search + Markdown formatting
-  Professional report output with sources

 Quick Start

Prerequisites
- Python 3.11+
- Telegram Bot Token
- Tavily API Key (free tier: 1000 queries/month)

 Installation

```bash
# Clone repo
git clone https://github.com/eueuw95/deep-research-bot.git
cd deep-research-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create `.env` file:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TAVILY_API_KEY=your_tavily_api_key
```

Get keys:
- Telegram: [@BotFather](https://t.me/BotFather)
- Tavily: [tavily.com](https://tavily.com) (free tier)

### Run Locally

```bash
python src/bot.py
```

##  Docker Deployment

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f
```

##  DigitalOcean Deployment

```bash
# On your DO droplet
git clone https://github.com/eueuw95/deep-research-bot.git
cd deep-research-bot

# Run deploy script
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

##  Usage

1. Search `@your_bot_name` on Telegram
2. Send `/start` for welcome message
3. Send `/research AI写作工具` to get report
4. Send `/quick 抖音算法` for quick summary

##  Project Structure

```
deep-research-bot/
├── src/
│   └── bot.py              # Main bot application
├── deploy/
│   ├── deploy.sh           # DO deployment script
│   └── setup-service.sh    # Systemd service setup
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container config
├── docker-compose.yml     # Docker orchestration
├── .env.example           # Environment template
└── README.md             # This file
```

##  Tech Stack

- **Backend**: Python 3.11 + python-telegram-bot
- **Search**: Tavily AI Search API
- **Formatting**: Markdown
- **Deployment**: Docker + DigitalOcean

##  Example Output

```markdown
# AI写作工具 - 营销研究报告

##  执行摘要
AI写作工具市场正在快速增长...

##  详细发现
...

##  参考来源
| # | 来源 | 链接 |
|---|------|------|
| 1 | OpenAI Blog | [链接](...) |
```

##  Development Timeline

- **Day 1**: OpenClaw environment setup, telegram bot connection
- **Day 2**: Research pipeline (Tavily search + Markdown formatting)
- **Day 3**: DigitalOcean deployment, webhook setup

##  Future Features

- [ ] Claude integration for advanced analysis
- [ ] 小红书/X(Twitter) scraping
- [ ] Multi-language support
- [ ] Scheduled reports

##  License

MIT License - feel free to use and modify!

##  Author

Created by [@eueuw95](https://github.com/eueuw95)
Mentor: Steve
