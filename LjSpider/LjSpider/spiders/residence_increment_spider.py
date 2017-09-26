#-*- encoding:utf-8 -*-

import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import time
import psycopg2
import datetime

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Mysql import *

from LjSpider.Exception.tryex import *

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
        #    'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def __init__(self):
        self.d_c = {}
        d_c_q = Mysql().query_by_sql('''
            select d.route d_r,c.route c_r,c.id
            from t_web_lj_district d,t_web_lj_community c
            where d.id=c.district_id
        ''')
        for dc in d_c_q:
            self.d_c[dc['d_r'] + '_' + dc['c_r']] = dc['id']


    def start_requests(self):
        url_list = []
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        csv_reader = csv.DictReader(codecs.open('esf_irt_2017-09-24.csv', 'r', encoding='utf-8'))
        for row in csv_reader:
            url_list.append(row['residence_url'])
            url_set = set(url_list)
        for url in url_set:
            rlt = Mysql().query_by_sql("select count(*) from t_web_lj_residence where url='%s'" % url)
            if rlt == []:
                yield Request(
                    url,
                    callback=self.get_residence_info
                )

    def get_residence_info(self, response):
        sr = Selector(response)
        r_district = tryex.split(sr.xpath('//*[@class="fl l-txt"]/a[3]/@href').extract_first(), '/', -2)
        r_community = tryex.split(sr.xpath('//*[@class="fl l-txt"]/a[4]/@href').extract_first(), '/', -2)

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
        item['community_id']     = self.d_c[r_district + '_' + r_community]
        yield item
