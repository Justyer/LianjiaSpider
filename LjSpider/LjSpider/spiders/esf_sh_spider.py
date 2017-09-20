#-*- encoding:utf-8 -*-

import re
import time
import psycopg2

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class EsfSHSpider(CrawlSpider):
    name = 'lj_get_esf_sh'
    start_urls = []
    custom_settings = {
        # 'JOBDIR': 'crawls/lj_get_esf-3',
        # 'LOG_FILE': 'logs/lj_esf_house.log',
        'DOWNLOADER_MIDDLEWARES':{
            'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
            'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def __init__(self):
        self.website = 'http://sh.lianjia.com/'

    def start_requests(self):
        # id_esf_url = Postgresql().query('lj_residence', ['id', 'esf_url'])
        id_esf_url = Postgresql().query_by_sql("select id,esf_url from lj_residence where url like 'http://sh.lianjia.com/%'")
        for id_, url in id_esf_url:
            if url != 'None':
                yield Request(
                    url,
                    meta={'id': id_},
                    callback=self.get_esf_url
                )

    def get_esf_url(self,response):
        esf_url = Selector(response).xpath('//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/ul/li[6]/a/@href').extract()

        for url in esf_url:
            yield Request(
                self.website + url,
                meta=response.request.meta,
                callback=self.get_esf_info
            )

        next_page_url = Selector(response).xpath('//*[@gahref="results_next_page"]/@href').extract_first()
        if next_page_url:
            yield Request(
                self.website + next_page_url,
                meta=response.request.meta,
                callback=self.get_esf_url
            )

    def get_esf_info(self, response):
        print 'Url:', response.url

        sr = Selector(response)
        item = EsfItem()
        item['house_type']        = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li[1]/span[2]/text()').extract_first()
        item['orientation']       = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li[3]/span[2]/text()').extract_first()
        item['area']              = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li[3]/span[2]/text()').extract_first()
        item['inner_area']        = None
        item['heating_style']     = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li[4]/span[2]/text()').extract_first()
        item['decoration']        = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li[2]/span[2]/text()').extract_first()
        item['floor']             = sr.xpath('/html/body/section/div[2]/aside/ul[1]/li[2]/div/p[2]/text()').extract_first()
        item['house_type_struct'] = None
        item['build_type']        = None
        item['build_struct']      = None
        item['household']         = None
        item['elevator']          = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li[2]/span[2]/text()').extract_first()

        item['ring_num']          = sr.xpath('/html/body/section/div[2]/aside/ul[2]/li[3]/span[2]/text()').extract_first()
        item['lj_num']            = sr.xpath('/html/body/section/div[2]/aside/ul[2]/li[6]/span[2]/text()').extract_first()

        name  = sr.xpath('/html/body/section/div[2]/aside/div[2]/div[1]/div/h2/a/text()').extract_first()
        phone = sr.xpath('/html/body/section/div[2]/aside/div[2]/div[1]/div/p[2]/span[1]/text()').extract_first()
        turn  = sr.xpath('/html/body/section/div[2]/aside/div[2]/div[1]/div/p[2]/span[3]/text()').extract_first()
        try:
            item['broker']        = name + ' ' + phone + ' ' + turn
        except:
            item['broker']        = None

        item['house_age']         = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[2]/ul/li[2]/span[2]/text()').extract_first()
        item['transaction_owner'] = None
        item['use']               = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[3]/ul/li[2]/span[2]/text()').extract_first()
        item['house_owner']       = None
        item['listing_time']      = None
        item['listing_price']     = sr.xpath('/html/body/section/div[2]/aside/div[1]/div[1]/span[1]/text()').extract_first()
        item['unit_price']        = sr.xpath('/html/body/section/div[2]/aside/div[1]/div[2]/p/span/text()').extract_first()
        item['last_deal']         = sr.xpath('//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[2]/ul/li[1]/span[2]/text()').extract_first()
        item['mortgage']          = None
        item['house_backup']      = None

        item['url']               = response.url
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())
        item['residence_name']    = sr.xpath('/html/body/section/div[2]/aside/ul[2]/li[4]/span[2]/span/a[1]/text()').extract_first()
        item['residence_id']      = response.request.meta['id']
        yield item
