#!/usr/bin/env python3
"""
Deep Research Bot - Pure Tavily Version (No Claude Required)
Marketing Research Pipeline powered by Tavily AI Search
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import aiohttp

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

TAVILY_API_URL = "https://api.tavily.com/search"


class ResearchPipeline:
    """Research pipeline using Tavily AI Search only"""
    
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not set in .env file")
    
    async def search(self, query: str, max_results: int = 10, search_depth: str = "advanced") -> Dict:
        """Perform Tavily AI search"""
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": True,
            "include_raw_content": True,
            "include_images": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(TAVILY_API_URL, json=payload, timeout=60) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Tavily API error {response.status}: {error_text}")
                return await response.json()
    
    def format_markdown_report(self, query: str, search_results: Dict) -> str:
        """Format search results into structured Markdown report"""
        
        answer = search_results.get('answer', 'No summary available')
        sources = search_results.get('results', [])
        
        # Build markdown report
        report = f"""# {query} - 营销研究报告

## 📋 执行摘要

{answer}

---

## 🔍 详细发现

基于 Tavily AI 搜索分析，以下是关键信息：

"""
        
        # Add top sources with details
        for i, source in enumerate(sources[:5], 1):
            title = source.get('title', 'Unknown')
            url = source.get('url', '')
            content = source.get('content', 'No content available')[:500]
            
            report += f"""### {i}. {title}

{content}...

🔗 [查看来源]({url})

---

"""
        
        # Add all sources section
        report += """## 📚 参考来源

| # | 来源 | 链接 |
|---|------|------|
"""
        
        for i, source in enumerate(sources, 1):
            title = source.get('title', 'Unknown')[:40]
            url = source.get('url', '#')
            report += f"| {i} | {title}... | [链接]({url}) |\n"
        
        report += f"""

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*数据来源: Tavily AI Search*
"""
        
        return report
    
    async def run(self, query: str, max_results: int = 10) -> Dict:
        """Execute full research pipeline"""
        logger.info(f"Starting research for: {query}")
        
        # Search
        search_results = await self.search(query, max_results=max_results)
        logger.info(f"Search completed: {len(search_results.get('results', []))} sources")
        
        # Format report
        report = self.format_markdown_report(query, search_results)
        
        return {
            "query": query,
            "markdown_report": report,
            "sources": search_results.get('results', []),
            "search_summary": search_results.get('answer', ''),
            "timestamp": datetime.now().isoformat()
        }


class DeepResearchBot:
    """Telegram Bot for Deep Research"""
    
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")
        
        self.pipeline = ResearchPipeline()
        self.application = Application.builder().token(self.token).build()
        
        # Register handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("research", self.research_cmd))
        self.application.add_handler(CommandHandler("quick", self.quick_cmd))
        self.application.add_handler(CommandHandler("help", self.help_cmd))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message"""
        welcome_text = """🤖 *Deep Research Bot* - 营销研究助手

Powered by *Tavily AI Search* 🔍

📋 可用命令：
• `/research <主题>` - 生成研究报告（30秒）
• `/quick <主题>` - 快速搜索摘要
• `/help` - 帮助信息

💡 示例：
```
/research AI写作工具市场
/research 2024新能源汽车趋势
/quick 抖音电商最新玩法
```

⚠️ *注意：报告使用 Markdown 格式，建议在桌面端 Telegram 查看效果最佳。*
"""
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        help_text = """📖 *使用指南*

*`/research <主题>`*
- 执行深度搜索（10个来源）
- 生成结构化 Markdown 报告
- 包含执行摘要、详细发现、参考来源
- 耗时：20-40秒

*`/quick <主题>`*
- 快速获取搜索摘要
- 5个关键来源
- 适合快速查证
- 耗时：10秒

*报告包含：*
✓ 执行摘要（AI生成）
✓ 详细发现
✓ 参考来源列表

*技术栈：*
Tavily AI Search - 智能搜索
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def research_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Deep research command"""
        query = " ".join(context.args)
        
        if not query:
            await update.message.reply_text(
                "❌ 请提供研究主题\n\n"
                "示例：`/research 短视频营销趋势`",
                parse_mode='Markdown'
            )
            return
        
        # Send status message
        status_msg = await update.message.reply_text(
            f"🔍 开始研究：*{query}*\n\n"
            f"⏱ 预计时间：30秒\n"
            f"📊 搜索深度：advanced\n"
            f"🤖 AI引擎：Tavily Search",
            parse_mode='Markdown'
        )
        
        try:
            # Execute research
            result = await self.pipeline.run(query, max_results=10)
            
            # Delete status message
            await status_msg.delete()
            
            # Send report
            report = result['markdown_report']
            
            # Split if too long (Telegram limit: 4096 chars)
            if len(report) > 4000:
                chunks = self._split_message(report)
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await update.message.reply_text(chunk, parse_mode='Markdown')
                    else:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=chunk,
                            parse_mode='Markdown'
                        )
            else:
                await update.message.reply_text(report, parse_mode='Markdown')
            
            # Send completion message
            await update.message.reply_text(
                f"✅ 研究完成！\n"
                f"📚 来源数量：{len(result['sources'])}\n"
                f"💡 使用 `/research <新主题>` 继续探索",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Research error: {e}", exc_info=True)
            await status_msg.edit_text(
                f"❌ 研究失败\n\n"
                f"错误：{str(e)[:200]}\n\n"
                f"请重试或联系管理员。",
                parse_mode='Markdown'
            )
    
    async def quick_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick search command"""
        query = " ".join(context.args)
        
        if not query:
            await update.message.reply_text(
                "❌ 请提供搜索内容\n\n"
                "示例：`/quick 抖音最新算法`",
                parse_mode='Markdown'
            )
            return
        
        status_msg = await update.message.reply_text(
            f"⚡ 快速搜索：*{query}*...",
            parse_mode='Markdown'
        )
        
        try:
            # Quick search (basic depth, fewer results)
            result = await self.pipeline.search(query, max_results=5, search_depth="basic")
            
            answer = result.get('answer', '未找到摘要')
            sources = result.get('results', [])
            
            response = f"""⚡ *快速搜索结果*

**{query}**

{answer}

📚 *来源 ({len(sources)})：*
"""
            
            for i, s in enumerate(sources[:5], 1):
                title = s.get('title', 'Unknown')[:40]
                url = s.get('url', 'N/A')
                response += f"\n{i}. [{title}...]({url})"
            
            await status_msg.edit_text(
                response, 
                parse_mode='Markdown', 
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Quick search error: {e}", exc_info=True)
            await status_msg.edit_text(
                f"❌ 搜索失败：{str(e)[:200]}",
                parse_mode='Markdown'
            )
    
    def _split_message(self, text: str, max_length: int = 4000) -> List[str]:
        """Split long message into chunks"""
        chunks = []
        current_chunk = ""
        
        for line in text.split('\n'):
            if len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk)
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def run(self):
        """Start the bot with webhook for production"""
        import os
        logger.info("Starting Deep Research Bot (Pure Tavily Version)...")
        
        # Check if webhook URL is set (for production)
        webhook_url = os.getenv("WEBHOOK_URL")
        port = int(os.getenv("PORT", "8443"))
        
        if webhook_url:
            # Production: Use webhook
            self.application.run_webhook(
                listen="0.0.0.0",
                port=port,
                webhook_url=webhook_url,
                allowed_updates=Update.ALL_TYPES
            )
        else:
            # Development: Use polling with drop_pending_updates
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True  # Clear old updates
            )


if __name__ == "__main__":
    bot = DeepResearchBot()
    bot.run()
