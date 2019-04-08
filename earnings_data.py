import requests
import re
from bs4 import BeautifulSoup as soup
#r = requests.get('https://seekingalpha.com/symbol/AAPL/earnings', proxies={'http':'50.207.31.221:80'}).text

r = requests.get('https://seekingalpha.com/symbol/AAPL/earnings').text
results = re.findall('Revenue of \$[a-zA-Z0-9\.]+', r)
s = soup(r, 'lxml')
titles = list(map(lambda x:x.text, s.find_all('span', {'class':'title-period'})))
epas = list(map(lambda x:x.text, s.find_all('span', {'class':'eps'})))
deciding = list(map(lambda x:x.text, s.find_all('span', {'class':re.compile('green|red')})))
results = list(map(list, zip(titles, epas, results, epas)))
print(results)