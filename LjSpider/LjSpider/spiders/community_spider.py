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
        'LOG_LEVEL': 'DEBUG',
        'FEED_URI': '/mnt/d/workspace/www/LianjiaSpider/LjSpider/community_fuck3.csv',
        'DOWNLOADER_MIDDLEWARES':{
           'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertMysqlPipeline': 300,
        #    'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def __init__(self):
        self.co_route = Mysql().query_by_sql('''
                            select route
                            from t_web_lj_community
                        ''')
        self.exist_route = [x['route'] for x in self.co_route]

    def start_requests(self):
        id_and_route = Mysql().query_by_sql('''
                            select di.id,di.route,ci.url
                            from t_web_lj_city ci,t_web_lj_district di
                            where di.city_id=ci.id and ci.id=7
                        ''')
        for one in id_and_route:
            yield Request(
                one['url'] + 'xiaoqu/' + one['route'] + '/',
                meta={'id': one['id']},
                callback=self.get_community,
                dont_filter=True
            )

    def get_community(self, response):
        district_id = response.meta['id']
        cn_name = Selector(response).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a/text()').extract()
        route = Selector(response).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a/@href').extract()
        item = CommunityItem()
        for n, r in zip(cn_name, route):
            rr = r.split('/')[2]
            print 'rrr:', rr
            # if rr not in self.exist_route:
            item['cn_name'] = n
            item['route'] = rr
            item['district_id'] = district_id
            yield item
