#-*- encoding:utf-8 -*-

import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import time
import psycopg2

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class ResidenceIrtSpider(CrawlSpider):
    name = 'lj_get_residence_irt'
    start_urls = []
    custom_settings = {
        # 'JOBDIR': 'crawls/lj_get_deal-1000-5000',
        # 'LOG_FILE': 'logs/lj_esf_transaction.log',
        'DOWNLOADER_MIDDLEWARES':{
            'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
           'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def __init__(self):
        self.d_c = {}

    def start_requests(self):
        csv_reader = csv.DictReader(codecs.open('../esf_irt_2017-09-22.csv', 'r', encoding='utf-8'))
        for row in csv_reader:
            rlt = Postgresql().query_by_sql("select count(*) from lj_residence where url='%s'" % row['residence_url'])
            if rlt == []:
                yield Request(
                    row['residence_url'],
                    callback=self.get_residence_info
                )

    def get_residence_info(self, response):
        sr = Selector(response)
        item = ResidenceItem()
        item['residence_name']   = sr.xpath('//*[@class="detailTitle"]/text()').extract_first()
        item['avg_price']        = sr.xpath('//*[@class="xiaoquUnitPrice"]/text()').extract_first()
        item['avg_time']         = sr.xpath('//*[@class="xiaoquUnitPriceDesc"]/text()').extract_first()
        item['address']          = sr.xpath('//*[@class="detailDesc"]/text()').extract_first()
        item['coordinate']       = sr.xpath('//*[@class="xiaoquInfoContent"]/span/@xiaoqu').extract_first()
        item['build_time']       = sr.xpath('//*[@class="xiaoquInfo"]/div[1]/span[2]/text()').extract_first()
        item['property_price']   = sr.xpath('//*[@class="xiaoquInfo"]/div[3]/span[2]/text()').extract_first()
        item['property_company'] = sr.xpath('//*[@class="xiaoquInfo"]/div[4]/span[2]/text()').extract_first()
        item['developer']        = sr.xpath('//*[@class="xiaoquInfo"]/div[5]/span[2]/text()').extract_first()
        item['total_buildings']  = sr.xpath('//*[@class="xiaoquInfo"]/div[6]/span[2]/text()').extract_first()
        item['total_houses']     = sr.xpath('//*[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract_first()
        item['url']              = response.url
        item['crawl_time']       = time.strftime("%Y-%m-%d %X",time.localtime())
        item['community_id']     = self.d_c[response.request.meta['d_c']]
        yield item
