import re
import psycopg2

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Mysql import *

class CommunitySpider(CrawlSpider):
    name = 'lj_get_community'
    start_urls = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
        #    'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
           'LjSpider.pipelines.InsertMysqlPipeline': 300
        }
    }

    def start_requests(self):
        Mysql().truncate_table('t_web_lj_community')
        id_and_route = Mysql().query_by_sql('''
                            select di.id,di.route,ci.url
                            from t_web_lj_city ci,t_web_lj_district di
                            where di.city_id=ci.id
                        ''')
        for one in id_and_route:
            yield Request(
                one['url'] + 'ershoufang/' + one['route'] + '/',
                meta={'id': one['id']},
                callback=self.get_community,
                dont_filter=True
            )

    def get_community(self, response):
        district_id = response.meta['id']
        cn_name = Selector(response).xpath('//*[@data-role="ershoufang"]/div[2]/a/text()').extract()
        route = Selector(response).xpath('//*[@data-role="ershoufang"]/div[2]/a/@href').extract()
        item = CommunityItem()
        for n, r in zip(cn_name, route):
            item['cn_name'] = n
            item['route'] = r.split('/')[2]
            item['district_id'] = district_id
            yield item
