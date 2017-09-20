import re
import psycopg2

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class CommunitySpider(CrawlSpider):
    name = 'lj_get_community'
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
        # id_and_route = Postgresql().query_by_sql('select di.id,di.route,ci.url from lj_city ci,lj_district di where di.city_id=ci.id')
        # for id_, route, url in id_and_route:
        #     yield Request(
        #         url + 'xiaoqu/' + route + '/',
        #         meta={'id': id_},
        #         callback=self.get_community
        #     )
        id_and_route = Postgresql().query_by_sql('select id,route from lj_district di where city_id=2')
        for id_, route in id_and_route:
            yield Request(
                'http://sh.lianjia.com/xiaoqu/' + route + '/',
                meta={'id': id_},
                callback=self.get_community,
                dont_filter=True
            )

    def get_community(self, response):
        # district_id = response.meta['id']
        # cn_name = Selector(response).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a/text()').extract()
        # route = Selector(response).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a/@href').extract()
        # item = CommunityItem()
        # for n, r in zip(cn_name, route):
        #     item['cn_name'] = n
        #     item['route'] = r.split('/')[2]
        #     item['district_id'] = district_id
        #     yield item
        district_id = response.meta['id']
        cn_name = Selector(response).xpath('//*[@id="filter-options"]/dl[1]/dd/div[2]/a/text()').extract()
        route = Selector(response).xpath('//*[@id="filter-options"]/dl[1]/dd/div[2]/a/@href').extract()
        item = CommunityItem()
        flag = False
        for n, r in zip(cn_name, route):
            if flag:
                item['cn_name'] = n
                item['route'] = r.split('/')[2]
                item['district_id'] = district_id
                yield item
            else:
                flag = True;
