# Scrapy Proxy Spider

### This project scrapes 150 free proxies and saves results

## Install dependencies:
```bash
pip install -r requirements.txt
```
### Copy .env.example to .env and put your USER_ID

## Run spider:
```bash
scrapy crawl freeproxy_spider
```

### Solution

- Built with Scrapy and Python
- Scrapes 150 free proxies and saves all proxies to `proxies.json`
- Splits proxies into batches of 29 and sends them via POST to the form
- Receives `save_id` for each batch and saves final mapping to `results.json`
- Logs total spider execution time in `time.txt`

All steps (scraping, posting, logging) are executed inside a single spider run
