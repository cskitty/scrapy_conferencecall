## Using Scrapy to Download Conference call from SeekingAlpha


## set up tor
sudo apt install tor


## create password for tor control port
tor --hash-password my_password
sudo nano /etc/tor/torrc

ControlPort 9051
# hashed password below is obtained via `tor --hash-password my_password`
HashedControlPassword 16:D75C686510440DCF60BB9DE09BBCC271E7C08613D25629A53C296CD057
CookieAuthentication 1

sudo service tor restart  

##install python-stem, used to interact with the Tor Controller
sudo apt-get install python-stem

## set up privproxy
sudo apt-get install privoxy


### Add the the following line:
sudo nano /etc/privoxy/config  

forward-socks5 / 127.0.0.1:9050 .  
forward-socks4a / 127.0.0.1:9050 .


## Restart the tor and privoxy service.
sudo service privoxy restart

## create virtualenv 
python -m virtualenv env

## activate the virtualenv
source env/bin/activate

## install python module requirements (scrapy, fake_useragent)
pip install -r requirements.txt

## scrapy

###test
scrapy crawl quotes_spider

###run
scrapy crawl earnings_spider