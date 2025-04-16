# Armenian Government News Scraper

This repository contains a modular Python application designed to scrape, summarize, and distribute news articles from official Armenian government sources. The tool supports automated scheduling, deduplication, and summarization using an LLM-based pipeline.

## 📦 Project Structure

```
├── chain.py
├── loader.pys
├── run_scraper.py
├── utils.py
├── pickle_files/
├── log_files/
```

## 🚀 Installation

1. (Optional) Create a virtual environment:

```bash
python -m venv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a .env file or set the variables in your environment:

```
OPENAI_API_KEY=key
BOT_TOKEN=telegram_token
CHANNEL_ID=telegram_channel_id
```

4. (Optional) Install as a local package:

```bash
pip install -e .
```
💡 **Note**: If this step fails with `ERROR: Can not execute setup.py since setuptools is not available`, fix it by running:
```bash
pip install --upgrade pip setuptools wheel
```

## How It Works

1. Every 3 hours, the script checks each source for updated articles.
2. If a new article is found (not in the cache), it:
   - Downloads the article content
   - Summarizes it using the LLM chain
   - Escapes the text for markdown-safe output
   - Sends the message (e.g., to Telegram, Slack, or console)


## 🏛 News Sources and URLs

| Source Name                                                | URL                                      |
|------------------------------------------------------------|------------------------------------------|
| Ministry of Foreign Affairs (MFA)                          | https://www.mfa.am/en/press-releases     |
| Ministry of Education, Science, Culture and Sports (ESCS)  | https://escs.am/en/news                  |
| Ministry of Defense (MIL)                                  | https://www.mil.am/en/news               |
| Ministry of Economy (MINECONOMY)                           | https://mineconomy.am/en/news            |
| Government of Armenia (GOV)                                | https://www.gov.am/en/news/              |


## 🛠 Usage

```bash
python run_scraper.py`
```
