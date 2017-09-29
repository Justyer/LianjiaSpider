import re

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class DistrictSpider(CrawlSpider):
    name = 'lj_get_district'
    start_urls = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
        #    'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
           'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
        #    'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def start_requests(self):
        # id_url = Postgresql().query_by_sql('select id,url from lj_city where id=1 or id=3 or id=4 or id=5 or id=6 or id=7 or id=10 or id=12 order by id asc')
        # for id_, url in id_url:
        #     yield Request(
        #         url + 'xiaoqu/',
        #         meta={'id': id_},
        #         callback=self.get_district
        #     )
        # yield Request(
        #     'http://sh.lianjia.com/xiaoqu/',
        #     meta={'id': 2},
        #     callback=self.get_district,
        #     dont_filter=True
        # )
        return [Request(
            'http://sh.lianjia.com/xiaoqu/',
            meta={'id': 2},
            callback=self.get_district,
            dont_filter=True
        )]

    def get_district(self, response):
        # cn_name = Selector(response).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a/text()').extract()
        # route = Selector(response).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a/@href').extract()
        # item = DistrictItem()
        # for n, r in zip(cn_name, route):
        #     item['cn_name'] = n
        #     item['route'] = r.split('/')[2]
        #     item['city_id'] = response.request.meta['id']
        #     yield item
        cn_name = Selector(response).xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/text()').extract()
        route = Selector(response).xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/@href').extract()
        item = DistrictItem()
        flag = False
        for n, r in zip(cn_name, route):
            if flag:
                item['cn_name'] = n
                item['route'] = r.split('/')[2]
                item['city_id'] = response.request.meta['id']
                yield item
            else:
                flag = True
