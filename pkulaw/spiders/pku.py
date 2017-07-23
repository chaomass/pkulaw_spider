# -*- coding: utf-8 -*-
import scrapy
import pymongo
from pkulaw.items import PkulawItem
from pkulaw.items import PkulawBrefItem
from scrapy.conf import settings
import re
import datetime

class PkuSpider(scrapy.Spider):
    name = 'pku'
    allowed_domains = ['www.pkulaw.cn']
    regurl = 'http://www.pkulaw.cn/case/Search/Record?Menu=CASE&IsFullTextSearch=False&MatchType=Exact&Keywords=&OrderByIndex=0&GroupByIndex=0&ShowType=1&ClassCodeKey=#ClassCode#%2C%2C#AreaCode#&Library=PFNL&Pager.PageSize=2000&Pager.PageIndex=0'
    start_urls = []

    def __init__(self,page_max=settings['PAGE_MAX_DEFAULT'],update=settings['UPDATE_DEFAULT'],*args, **kwargs):
        self.page_max = int(page_max)
        #self.update = 'true' == update.lower()
        #self.connection_string = "mongodb://%s:%d" % (settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        #self.client = pymongo.MongoClient(self.connection_string)
        #self.db = self.client[settings['MONGODB_DB']]
        #self.collection = self.db[settings['MONGODB_COLLECTION']]
        #ClassCodes = ['001','002','003','004','005','006']
        ClassCodes = ['001']
        AreaCodes = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36']
        for classcode in ClassCodes:
            for areacode in AreaCodes:
                url1 =  self.regurl.replace('#ClassCode#',classcode)
                url = url1.replace('#AreaCode#',areacode)
                self.start_urls.append(url)
        #print "start_urls_num:",len(self.start_urls)
        
    def closed(self,reason):
        self.close()
    
    def parse(self, response):
        total_pages = response.xpath('//span[@class="qp_totalnumber"]/text()').re('\d+')[1]
        #print "responseurl:",response.url
        if self.page_max == 1:
            end_page = int(total_pages)
        else:
            end_page = self.page_max
        #print "total_pages:",total_pages
        for n in range(1,end_page + 1):
            strinfo = re.compile('Pager.PageIndex=\d+')
            url =  strinfo.sub('Pager.PageIndex='+str(n),response.url)
            #print "url+++++++:",url
            yield scrapy.Request(url, self.parse_list)
    
    def parse_list(self,response):
        links = response.xpath('//body/dl/dd')
        #print links
        itembref = PkulawBrefItem()
        for url in links:
           # print "url:",url.xpath('a/@href').extract()
            try:
                gid=re.findall(r'_(.*?).html',url.extract())[0]
                itembref['title'] = url.xpath('a/text()').extract()[0]
                itembref['gid'] = gid
                itembref['court'] = url.xpath('div/p/span/text()').extract()[0]
                itembref['uid'] = url.xpath('div/p/span/text()').extract()[1]
                itembref['closedate'] =url.xpath('div/p/span/text()').extract()[2]
                itembref['casekind1'] = url.xpath('div/div/div/ul/li/a/text()').extract()[0]
                itembref['casekind2'] = url.xpath('div/div/div/ul/li/a/text()').extract()[1]
                itembref['casekind3'] = url.xpath('div/div/div/ul/li/a/text()').extract()[-4]
                itembref['casekindno'] = url.xpath('div/div/div/ul/li/a/@href').extract()[-4].split('=')[1]
                #print "casekindno:",url.xpath('div/div/div/ul/li/a/@href').extract()[-4].split('=')[1]
                itembref['czjb'] = url.xpath('div/div/div/ul/li/a/text()').extract()[-3]
                itembref['slcx'] = url.xpath('div/div/div/ul/li/a/text()').extract()[-2]
                itembref['wslx'] = url.xpath('div/div/div/ul/li/a/text()').extract()[-1]
                itembref['rksj'] = str(datetime.datetime.now())
                yield itembref
                ex_href='http://www.pkulaw.cn/case/FullText/_getFulltext?library=pfnl&gid=#gid#&loginSucc=0'
                href=ex_href.replace('#gid#',gid)
                yield scrapy.Request(href, self.parse_detail)
            except Exception,e:
                print "exception in parselist:",e

    def parse_detail(self,response):
        item = PkulawItem()
        item['gid'] = re.findall(r'gid=(.*?)&loginSucc=0',response.url)[0]
        item['urls'] = response.url
        item['uid'] = response.xpath('//body/div[2]/text()').extract()[0]
        item['text'] = response.xpath('//body')[0].extract()
        item['title'] = response.xpath('//p/font[@class="MTitle"]/text()').extract()[0]
        #item['bug_type'] = response.xpath('//*[@id="bugDetail"]/div[5]/h3[7]/text()').extract()[0].split(u'：')[1].strip()
        #some author not text,for examp:
        #http://wooyun.org/bugs/wooyun-2010-01010
        #there will be error while parse author,so do this

        #the response.body type is str,so we need to convert to utf-8
        #if not utf-8,saving to mongodb may have some troubles
        item['html'] = response.body.decode('utf-8','ignore')
        #dt = response.xpath("//h3[@class='wybug_date']/text()").re("[\d+]{4}-[\d+]{2}-[\d+]{2}")[0].split('-')
        return item

    def __search_mongodb(self,gid):
        #
        gid_exsist = True if self.collection.find({'gid':gid}).count()>0 else False
        #
        return gid_exsist
