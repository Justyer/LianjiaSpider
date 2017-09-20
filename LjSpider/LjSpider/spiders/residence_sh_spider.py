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

class ResidenceSHSpider(CrawlSpider):
    name = 'lj_get_residence_sh'
    start_urls = [
        'http://sh.lianjia.com/xiaoqu/'
    ]
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
        self.website = 'http://sh.lianjia.com'

    def start_requests(self):
        q_result = Postgresql().query_by_sql('''
                            select co.id,co.route
                            from lj_community co,lj_district di
                            where co.district_id=di.id and di.city_id=2
                        ''')

        for id_, route in q_result:
            yield Request(
                self.start_urls[0] + route + '/',
                callback=self.get_residence_url,
                dont_filter=True
            )

    def get_residence_url(self,response):
        li = Selector(response).xpath('//*[@id="house-lst"]/li').extract()
        for l in li:
            st = Selector(text=l)
            url = st.xpath('//*[@class="pic-panel"]/a/@href').extract_first()
            district = st.xpath('//*[@class="info-panel"]/div[1]/div[2]/div/a[1]/@href').extract_first().split('/')[-2]
            community = st.xpath('//*[@class="info-panel"]/div[1]/div[2]/div/a[2]/@href').extract_first().split('/')[-2]
            yield Request(
                self.website + url,
                meta={'d_c': district + '_' + community},
                callback=self.get_residence_info,
                dont_filter=True
            )

        next_page_url = Selector(response).xpath('//*[@gahref="results_next_page"]/@href').extract_first()
        if next_page_url:
            yield Request(
                self.website + next_page_url,
                callback=self.get_residence_url,
                dont_filter=True
            )

    def get_residence_info(self, response):
        sr = Selector(response)
        item = ResidenceItem()
        item['name']             = sr.xpath('/html/body/div[4]/div[1]/section/div[1]/div[1]/span/h1/text()').extract_first()

        avg_price = sr.xpath('//*[@id="zoneView"]/div[2]/div[2]/div/p[2]/span[1]/text()').extract_first()
        if avg_price:
            item['avg_price']    = avg_price.strip()
        else:
            item['avg_price']    = None

        item['avg_time']         = None
        item['address']          = sr.xpath('/html/body/div[4]/div[1]/section/div[1]/div[1]/span/span[2]/text()').extract_first()
        item['coordinate']       = sr.xpath('//*[@id="actshowMap_xiaoqu"]/@xiaoqu').extract_first()

        build_time = sr.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[2]/span/span/text()').extract_first()
        if avg_price:
            item['build_time']   = build_time.strip()
        else:
            item['build_time']   = None

        property_price = sr.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[3]/span/text()').extract_first()
        if avg_price:
            item['property_price'] = property_price.strip()
        else:
            item['property_price'] = None

        property_company = sr.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[4]/span/text()').extract_first()
        if avg_price:
            item['property_company'] = property_company.strip()
        else:
            item['property_company'] = None

        developer = sr.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[5]/span/text()').extract_first()
        if avg_price:
            item['developer']    = developer.strip()
        else:
            item['developer']    = None

        item['floor_sum']        = None
        item['house_sum']        = None

        esf_url = sr.xpath('//*[@id="yz_ershoufang"]/div[1]/a/@href').extract_first()
        if esf_url:
            item['esf_url']      = self.website + esf_url
        else:
            item['esf_url']      = None
        item['deal_url']         = None
        item['url']              = response.url
        item['crawl_time']       = time.strftime("%Y-%m-%d %X",time.localtime())
        item['community_id']     = self.d_c[response.request.meta['d_c']]
        yield item
