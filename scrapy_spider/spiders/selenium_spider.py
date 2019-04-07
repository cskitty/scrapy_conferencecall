import scrapy
from selenium.webdriver import Firefox
from scrapy_spider.pipelines import ScrapySpiderPipeline


class SeleniumSpider(scrapy.Spider):
    name = "selenium_spider"

    def __init__(self):
        self.driver = Firefox()

    def start_requests(self):
        #get all the downloaded page set from mongodb
        curs = ScrapySpiderPipeline().get_urls_from_page("1")
        for cur in curs:
            if cur["text"] != "":
                continue
            else:
                yield scrapy.Request(url= "https://www.google.com", callback=self.parse, dont_filter=True, meta={'id': str(cur['_id']), "url": cur["url"]})

    def parse(self, response):
        #self.driver.get(response.url)
        self.driver.get(response.meta['url'])

        data = self.driver.find_elements_by_css_selector("div#content-rail article #a-body")
        print('data')
        #data = data[0].extract()

        id = response.meta['id']

        print('text = ', data[0])

        ScrapySpiderPipeline().update_with_text(id, "test abc")
        print("[OK] ", response.url)
        self.driver.quit()