#-*- encoding:utf-8 -*-

import codecs
import datetime

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Mysql import *

from LjSpider.Exception import tryex

class TestSpider(CrawlSpider):
    name = 'sys_test'
    start_urls = [
        'http://118.190.22.19',
        'https://bj.lianjia.com/xiaoqu/1111047349969/',
        'https://nj.lianjia.com/ershoufang/103101703194.html',
        'https://nj.lianjia.com/chengjiao/103101536973.html',
        'http://sh.lianjia.com/xiaoqu/dahua/',
        'https://wh.lianjia.com/ershoufang/104100580150.html',
        'https://bj.lianjia.com/xiaoqu/andingmen/',
        'https://bj.lianjia.com/chengjiao/101100788395.html',
        'https://bj.lianjia.com/chengjiao/101101012718.html',
        'https://bj.lianjia.com/xiaoqu/1111027375686/',
    ]
    custom_settings = {
        # 'FEED_URI': '/usr/local/crawler/dxc/common/lj/data/lj_test_%s.csv' % datetime.datetime.now(),
        # 'JOBDIR': '/usr/local/crawler/dxc/common/lj/crawls/lj_test_%s' % datetime.datetime.now(),
        # 'LOG_FILE': '/usr/local/crawler/dxc/common/lj/logs/lj_test_%s.log' % datetime.datetime.now(),
        'DOWNLOADER_MIDDLEWARES':{
            # 'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertMysqlPipeline': 300,
        }
    }

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.test_page,
            dont_filter=True
        )]

    def test_page(self, response):
        is_exist = Mysql().query_by_sql("select url from t_web_lj_residence where url='https://bj.lianjia.com/xiaoqu/1111027375686/'")
        # print 'kong2:', type(Mysql().query_by_sql("select url from t_web_lj_residence where url='https://bj.lianjia.com/xiaoqu/1111027375686/'"))
        if isinstance(is_exist, list):
            print 'list_a'
        else:
            print 'tuple_a'
        # fil = codecs.open('/usr/local/crawler/dxc/I.txt', 'a', encoding='utf-8')
        # fil.write('I am I.')
        # fil.close()
