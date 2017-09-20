#-*- encoding:utf-8 -*-

import re
import psycopg2

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class CountSpider(CrawlSpider):
    name = 'lj_get_count'
    start_urls = []
    custom_settings = {
        # 'JOBDIR': 'crawls/lj_get_deal-1000-5000',
        # 'LOG_FILE': 'logs/lj_esf_transaction.log',
        'DOWNLOADER_MIDDLEWARES':{
            # 'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
        }
    }

    def start_requests(self):
        id_url = Postgresql().query_by_sql('''
                                select c.id,c.cn_name,c.route
                                from lj_community c,lj_district d
                                where c.district_id=d.id and d.city_id=2;
                            ''')
        for id_, name, route in id_url:
            yield Request(
                'http://sh.lianjia.com/xiaoqu/' + route + '/',
                meta={'id': id_, 'name': name},
                callback=self.get_count,
                dont_filter=True
            )

    def get_count(self,response):
        count = Selector(response).xpath('//*[@class="list-head clear"]/h2/span/text()').extract_first()
        item = DealCountItem()
        item['name'] = response.request.meta['name']
        item['count'] = str(count)
        item['page'] = None
        item['residence_id'] = response.request.meta['id']
        yield item
