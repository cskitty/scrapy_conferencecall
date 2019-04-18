## Using Scrapy to Download Conference call from SeekingAlpha


## set up tor
sudo apt install tor

## create password for tor control port
tor --hash-password my_password

HashedControlPassword 16:D75C686510440DCF60BB9DE09BBCC271E7C08613D25629A53C296CD057
CookieAuthentication 1

##update password in tor config file
sudo nano /etc/tor/torrc

##restart tor service
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

###run and output to json
scrapy crawl url_spider -o conf.json -t json


#Mongodb

## install mongodb
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4  
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list  
sudo apt-get update  
sudo apt-get install -y mongodb-org  

###launch as daemon:  
sudo ln -sf /opt/mongodb/ /var/lib/mongodb  
sudo chown -R mongodb:mongodb /var/lib/mongodb  
sudo chown -R mongodb:mongodb /opt/mongodb
sudo service mongod start  


###launch as a program:  
mongod --dbpath /opt/mongodb/  


###launch command shell  
mongodb  

