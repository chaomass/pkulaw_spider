# pkulaw_spider
基于Ubuntu 16.04、scrapy
依赖：
+ python 2.7和pip
+ mongodb
+ scrapy 
+ pymongo

步骤
--------
1、安装python、pip、mongodb

```bash
sudo apt-get install python python-pip mongodb
```
2、安装scrapy

```bash
安装scrapy如果报错，则先apt-get安装下述依赖包，然后安装pip安装lxml后即可正常安装scrapy
sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev libevent-dev python-openssl

sudo pip install lxml
sudo pip install scrapy
```
3、安装pymongo

```bash
sudo pip install pymongo

4、从github下载源码
```bash
git clone https://github.com/chaomass/pkulaw_spider.git
