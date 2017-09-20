import re

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *

class CitySpider(CrawlSpider):
    name = 'lj_get_city'
    start_urls = [
        'https://bj.lianjia.com/'
    ]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
           #'LjSpider.middleware.ProxyForMainMiddleware': 543,
        },
        'ITEM_PIPELINES':{
           'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
        #    'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.get_city
        )]

    def get_city(self, response):
        item = CityItem()

        cn_name = Selector(response).xpath('/html/body/div[1]/div/div[2]/div[3]/div[1]/ul/li/div/a/text()').extract()
        route = Selector(response).xpath('/html/body/div[1]/div/div[2]/div[3]/div[1]/ul/li/div/a/@href').extract()
        for n, r in zip(cn_name, route):
            item['cn_name'] = n
            item['route'] = r[8:].split('.')[0]
            item['url'] = r
            yield item

        cn_name = Selector(response).xpath('/html/body/div[1]/div/div[2]/div[3]/div[2]/ul/li/div/a/text()').extract()
        route = Selector(response).xpath('/html/body/div[1]/div/div[2]/div[3]/div[2]/ul/li/div/a/@href').extract()
        for n, r in zip(cn_name, route):
            item['cn_name'] = n
            item['route'] = r[8:].split('.')[0]
            item['url'] = r
            yield item
