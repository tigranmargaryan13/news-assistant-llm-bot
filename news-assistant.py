import asyncio
import time
from datetime import datetime
from typing import Optional

from loaders.chain import load_chain
from utils import send_message, escape_markdown_v2
from loaders.gov_loader import NewsLoader
from loaders.config import settings


FETCH_INTERVAL_HOURS = 3
TRIGGER_MINUTE = 59
SLEEP_AFTER_EXECUTION_SECONDS = 60 * 60 * 4.9
POLLING_INTERVAL_SECONDS = 30


loader = NewsLoader()
chain = load_chain()

loader.logger.info("News monitoring started.")
loader.logger.info("-" * 60)


def process_article(full_article: Optional[str], link: Optional[str], source: str) -> Optional[str]:
    """
    Summarizes and escapes article content if available.

    Args:
        full_article (str | None): The raw full article content.
        link (str | None): The source URL of the article.
        source (str): The source identifier.

    Returns:
        str | None: The processed and formatted message ready to send.
    """
    if full_article:
        summarized = chain.invoke(full_article)
        escaped_msg = escape_markdown_v2(summarized.content)
        escaped_msg = escaped_msg.replace("SOURCELINK", f"[SOURCE]({link})")
        loader.logger.info(f"{source} ✅ New article processed.")
        return escaped_msg
    else:
        loader.logger.info(f"{source} 🕰 No updates.")
        return None


def should_run(now: datetime) -> bool:
    """Determines whether the current time matches the update schedule."""
    return now.hour % FETCH_INTERVAL_HOURS == 0 and now.minute == TRIGGER_MINUTE


if __name__ == "__main__":
    while True:
        current_time = datetime.now()

        #TODO move to cron
        if should_run(current_time):
            for source in settings.NEWS_SOURCES:
                article, link = loader.get_latest_article_if_updated(source)
                message = process_article(article, link, source)
                if message:
                    asyncio.run(send_message(message))
            loader.logger.info("-" * 60)
            time.sleep(SLEEP_AFTER_EXECUTION_SECONDS)
        else:
            time.sleep(POLLING_INTERVAL_SECONDS)
