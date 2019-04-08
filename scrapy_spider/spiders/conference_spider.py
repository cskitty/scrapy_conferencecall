import scrapy
from scrapy_spider.pipelines import ScrapySpiderPipeline


class SeleniumSpider(scrapy.Spider):
    name = "conference_spider"
    download_delay = 1.0
    custom_settings = {
            'LOG_LEVEL': 'DEBUG', #'CRITICAL', #
            'LOG_ENABLED': True,
            'DOWNLOAD_DELAY':1 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
    }

    def start_requests(self):
        #get all the downloaded page set from mongodb
        unique_pages = ScrapySpiderPipeline().get_unique_page_set()

        for page in unique_pages:
            curs = ScrapySpiderPipeline().get_urls_from_page(page)
            for cur in curs:
                if cur["text"] != "":
                    continue
                else:
                    yield scrapy.Request(url=cur["url"], callback=self.parse, meta={"id":str(cur["_id"])})

    def parse(self, response):
        data = response.css("div#content-rail article #a-body")
        data = data.extract()

        #print('text = ', data[0])
        ScrapySpiderPipeline().update_with_text(response.meta['id'], data[0])