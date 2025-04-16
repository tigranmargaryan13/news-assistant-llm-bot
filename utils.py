import re
from telegram import Bot
from loaders.config import settings


def escape_markdown_v2(text):
    """Escape special characters for Telegram MarkdownV2."""
    escape_chars = r'_[]()~`>#+-=|{}.!'

    filtered_message = re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)
    escaped_message = filtered_message.replace("**", "*")

    return escaped_message

async def send_message(message):
    bot = Bot(token=settings.BOT_TOKEN)
    await bot.send_message(
        chat_id=settings.CHANNEL_ID,
        text=message,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
    )

    print("Message sent successfully!")
