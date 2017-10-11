import re

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Mysql import *

class DistrictSpider(CrawlSpider):
    name = 'lj_get_district'
    start_urls = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
        #    'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
           'LjSpider.pipelines.InsertMysqlPipeline': 300,
        }
    }

    def __init__(self):
        self.buyao = [
            'https://lf.lianjia.com/ershoufang/yanjiao/',
            'https://lf.lianjia.com/ershoufang/xianghe/'
        ]

    def start_requests(self):
        Mysql().truncate_table('t_web_lj_district')
        id_url = Mysql().query_by_sql('''
                    select id,url
                    from t_web_lj_city
                    where url is not null
                ''')
        for iu in id_url:
            yield Request(
                iu['url'] + 'ershoufang/',
                meta={'id': iu['id']},
                callback=self.get_district,
                dont_filter=True
            )

    def get_district(self, response):
        cn_name = Selector(response).xpath('//*[@data-role="ershoufang"]/div/a/text()').extract()
        route = Selector(response).xpath('//*[@data-role="ershoufang"]/div/a/@href').extract()
        item = DistrictItem()
        for n, r in zip(cn_name, route):
            if r not in self.buyao:
                item['cn_name'] = n
                item['route'] = r.split('/')[2]
                item['city_id'] = response.request.meta['id']
                yield item
