import re
import pickle
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


class NewsLoader:
    """
    A class for scraping, parsing, and caching news articles from
    official Armenian government websites.
    """
    BASE_URLS = {
        'MFA': 'https://www.mfa.am',
        'ESCS': 'https://escs.am',
        'MIL': 'https://www.mil.am',
        'MINECONOMY': 'https://www.mineconomy.am',
        'GOV': 'https://www.gov.am',
    }

    NEWS_FEED_URLS = {
        'MFA': f"{BASE_URLS['MFA']}/en/",
        'ESCS': f"{BASE_URLS['ESCS']}/en/category/news",
        'MIL': f"{BASE_URLS['MIL']}/en/news",
        'MINECONOMY': f"{BASE_URLS['MINECONOMY']}/en/news",
        'GOV': f"{BASE_URLS['GOV']}/en/news",
    }

    CACHE_PATHS = {
        'MFA': 'pickle_files/mfa_article_links.pkl',
        'ESCS': 'pickle_files/escs_article_links.pkl',
        'MIL': 'pickle_files/mil_article_links.pkl',
        'MINECONOMY': 'pickle_files/mineconomy_article_links.pkl',
        'GOV': 'pickle_files/gov_article_links.pkl',
    }

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler("log_files/official_news.log", mode="w")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        ))
        self.logger.addHandler(handler)

    def get_soup(self, url: str) -> BeautifulSoup:
        """Takes a URL and returns its BeautifulSoup"""
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def parse_news_with_links(self, soup: BeautifulSoup, source: str) -> List[Dict[str, str]]:
        """
        Parses all news articles' titles, dates, and links from the news listing page.

        Args:
            soup (BeautifulSoup): Parsed HTML content of the news page.
            source (str): One of 'MFA', 'ESCS', 'MIL', 'MINECONOMY', or 'GOV'.

        Returns:
            List[Dict[str, str]]: A list of news entries with title, date, and link.
        """
        news_items_list = []

        try:
            if source == 'MFA':
                for item in soup.select("div.home-news-listing li.home-news-item"):
                    title_tag = item.select_one("a.link")
                    news_items_list.append({
                        "title": title_tag.get_text(strip=True) if title_tag else "No Title",
                        "date": item.select_one("div.date").get_text(strip=True),
                        "link": title_tag['href'],
                    })

            elif source == 'ESCS':
                for item in soup.select("div.form-row.cnews article.col.w-100"):
                    title = item.select_one("div.title.text-start").get_text(strip=True)
                    link = item.select_one("a.d-block.clearfix")['href']
                    date = item.select_one("time.text-start").get_text(strip=True)
                    news_items_list.append({
                        "title": title,
                        "date": date,
                        "link": link,
                    })

            elif source == 'MIL':
                for item in soup.select("section.news-section div.news-list-artical"):
                    title_tag = item.select_one("h3 > a")
                    date_tag = item.select_one("div.news-action > p")
                    news_items_list.append({
                        "title": title_tag.get_text(strip=True),
                        "date": date_tag.get_text(strip=True),
                        "link": title_tag['href'],
                    })

            elif source == 'MINECONOMY':
                for item in soup.select("div.news-content div.news-background-text"):
                    title_tag = item.find("h2")
                    a_tag = title_tag.find_parent("a", href=True) if title_tag else None
                    date_tag = item.find("div", class_="date")
                    news_items_list.append({
                        "title": title_tag.get_text(strip=True),
                        "date": date_tag.get_text(strip=True),
                        "link": a_tag["href"],
                    })

            elif source == 'GOV':
                for item in soup.select("div#content div.news"):
                    title_tag = item.select_one("strong")
                    link_tag = item.find("a", string=re.compile(r"more\s*»", re.I))
                    date_tag = item.find("p", class_="news-date")
                    news_items_list.append({
                        "title": title_tag.get_text(strip=True),
                        "date": date_tag.get_text(strip=True).split(" ", 1)[-1],
                        "link": link_tag["href"],
                    })

        except Exception as e:
            self.logger.error(f"Error while parsing news from {source}: {e}")

        return news_items_list

    def get_article_content(self, article_url: str, source: str) -> str:
        """
        Extracts and returns the full content of a news article.

        Args:
            article_url (str): The URL of the article.
            source (str): The source identifier.

        Returns:
            str: Article text.
        """
        soup = self.get_soup(article_url)

        try:
            if source == 'MFA':
                content = "\n".join(p.get_text(strip=True) for p in soup.select('p[style="text-align: justify;"]'))
                title = soup.find("h2").get_text(strip=True)

            elif source == 'ESCS':
                title = soup.find("title").get_text(strip=True)
                body = soup.find("div", class_="article-text form-row")
                if body:
                    content = "\n".join(p.get_text(strip=True) for p in body.find_all("p"))

            elif source == 'MIL':
                title = soup.title.get_text(strip=True)
                body = soup.find("div", class_="text-box")
                content = body.get_text(strip=True).replace("<br/>", "\n")

            elif source == 'MINECONOMY':
                header = soup.find("div", class_="full-news-header")
                title = header.find("h1").get_text(strip=True)
                body = soup.find("div", class_="full-news-text")
                content = body.get_text(strip=True)

            elif source == 'GOV':
                title = soup.title.get_text(strip=True)
                content = "\n".join(p.get_text(strip=True) for p in soup.select("p[style='text-align: justify;']"))

        except Exception as e:
            self.logger.error(f"Failed to parse content from {article_url}: {e}")

        return f"# {title}\n\n{content}"

    def fetch_latest_articles(self, source: str) -> List[Dict[str, str]]:
        """
        Downloads the latest list of articles from a given source.

        Args:
            source (str): The identifier for the source site.

        Returns:
            List[Dict[str, str]]: Latest parsed articles.
        """
        news_url = self.NEWS_FEED_URLS.get(source)
        soup = self.get_soup(news_url)
        return self.parse_news_with_links(soup, source)

    def get_latest_article_if_updated(self, source: str) -> Optional[tuple[str, str]]:
        """
        Compares current and previous periods, returns new content if found.

        Args:
            source (str): The news source identifier.

        Returns:
            Optional[tuple[str, str]]: Full article content and link if updated, else None.
        """
        latest_articles = self.fetch_latest_articles(source)
        cache_path = self.CACHE_PATHS.get(source)

        try:
            with open(cache_path, "rb") as f:
                cached_articles = pickle.load(f)
        except FileNotFoundError:
            cached_articles = []

        if latest_articles != cached_articles:
            with open(cache_path, "wb") as f:
                pickle.dump(latest_articles, f)
            top_article_url = latest_articles[0]['link']
            content = self.get_article_content(top_article_url, source)
            return content, top_article_url

        return None, None
