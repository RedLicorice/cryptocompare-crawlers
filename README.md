## Cryptocurrency Crawlers

 Crawlers for Cryptocurrency-related APIs:
 - Cryptocompare social stats
 - Google Trends

**Prerequisites**

Setup .env according to .env.example

```$ cp .env.example .env```

```$ nano .env```

Install required packages

```$ pip3 install -r requirements.txt```

**Running**

Launch driver.py to start scraping.

<commands> can be any combination of:

- 'social' : Scrape social stats from cryptocompare
- 'trends' : Scrape Google Trends history

```$ python3 driver.py <commands>```
