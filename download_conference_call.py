import scrapy
from selenium.webdriver import firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
browser = firefox(Options=opts)
browser.get('https://seekingalpha.com/article/4251445-osmotica-pharmaceuticals-plc-osmt-ceo-brian-markison-q4-2018-results-earnings-call-transcript')


data = browser.find_elements_by_css_selector("div#content-rail article #a-body")
data = data.extract()