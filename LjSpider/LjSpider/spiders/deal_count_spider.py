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

class DealCountSpider(CrawlSpider):
    name = 'lj_get_count2'
    start_urls = [
        'https://nj.lianjia.com/chengjiao/'
    ]
    custom_settings = {
        # 'JOBDIR': 'crawls/lj_get_deal-1000-5000',
        # 'LOG_FILE': 'logs/lj_esf_transaction.log',
        'DOWNLOADER_MIDDLEWARES':{
            # 'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
        #    'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def start_requests(self):
        deal_new = Postgresql().query_by_sql('''select co.id,co.cn_name,co.route
                                                from lj_district d,lj_community co
                                                where d.id=co.district_id and d.city_id=3
                                        ''')

        for c_id, name, route in deal_new:
            yield Request(
                self.start_urls[0] + route + '/',
                meta={'id': c_id, 'route': route, 'name': name},
                callback=self.get_count2,
                dont_filter=True
            )

    def get_count2(self,response):
        count = Selector(response).xpath('//*[@class="total fl"]//span/text()').extract_first().strip()
        page = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]/@page-data').extract_first()
        if page:
            page = eval(page)['totalPage']
        item = DealNewCountItem()
        item['name']         = response.request.meta['name']
        item['route']        = response.request.meta['route']
        item['count']        = str(count)
        item['page']         = str(page)
        item['url']          = response.url
        item['community_id'] = response.request.meta['id']
        yield item
