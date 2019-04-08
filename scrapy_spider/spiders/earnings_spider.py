import scrapy
from scrapy_spider.pipelines import ScrapySpiderPipeline
import re
from bs4 import BeautifulSoup as soup

class EarningsSpider(scrapy.Spider):
    name = "earnings_spider"
    download_delay = 3.0
    custom_settings = {
            #'LOG_LEVEL': 'DEBUG', #'CRITICAL', #
            'LOG_ENABLED': True,
            'DOWNLOAD_DELAY':3 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
    }
    pipeline = ScrapySpiderPipeline()

    def start_requests(self):
        #get all the downloaded page set from mongodb
        print("starting")
        all_tickers = self.pipeline.get_unique_ticker_set_from_url_col()
        downloaded_tickers = self.pipeline.get_unique_ticker_set_from_earnings_col()

        print("all tickers ", all_tickers)
        for ticker in all_tickers:
            if ticker in downloaded_tickers:
                print("already downloaded ", ticker)
                continue
            else:
                print('downloading for ticker ', ticker)
                download_url = 'https://seekingalpha.com/symbol/'+ticker+'/earnings'
                yield scrapy.Request(url=download_url, callback=self.parse, meta={"ticker":ticker})

    def parse(self, response):
        results = re.findall('Revenue of \$[a-zA-Z0-9\.]+', response.text)
        s = soup(response.text, 'lxml')
        titles = list(map(lambda x: x.text, s.find_all('span', {'class': 'title-period'})))
        eps = list(map(lambda x: x.text, s.find_all('span', {'class': 'eps'})))
        deciding = list(map(lambda x: x.text, s.find_all('span', {'class': re.compile('green|red')})))
        results = list(map(list, zip(titles, eps, results, eps)))
        print('deciding=',deciding)
        print('results=',results)

        ticker =  response.meta["ticker"]
        f = open(ticker+".html", "w")
        f.write(response.text)
        f.close()
        #print('text = ', data[0])
        #ScrapySpiderPipeline().update_with_text(response.meta['id'], data[0])