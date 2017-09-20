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

class ResidenceSpider(CrawlSpider):
    name = 'lj_get_residence'
    start_urls = [
        'https://bj.lianjia.com/xiaoqu/'
    ]
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
        q_result = Postgresql().query_by_sql('''
                            select co.id,di.route,co.route
                            from lj_community co,lj_district di
                            where co.district_id=di.id and di.city_id=1;
                        ''')
        route_list = []
        for id_, d_route, c_route in q_result:
            self.d_c[d_route + '_' + c_route] = id_
            route_list.append(c_route)

        for route in route_list:
            yield Request(
                self.start_urls[0] + route + '/',
                callback=self.get_residence_url
            )

    def get_residence_url(self,response):
        li = Selector(response).xpath('/html/body/div[4]/div[1]/ul/li').extract()
        for l in li:
            st = Selector(text=l)
            url = st.xpath('//*[@class="img"]/@href').extract_first()
            district = st.xpath('//*[@class="district"]/@href').extract_first().split('/')[-2]
            community = st.xpath('//*[@class="bizcircle"]/@href').extract_first().split('/')[-2]
            yield Request(
                url,
                meta={'d_c': district + '_' + community},
                callback=self.get_residence_info
            )
        page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(Selector(text=page_box).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(Selector(text=page_box).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                yield Request(
                    response.url[0:response.url.find('/', 30) + 1] + 'pg' + str(curPage + 1) + '/',
                    callback=self.get_residence_url
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
