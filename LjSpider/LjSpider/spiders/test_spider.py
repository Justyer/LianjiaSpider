#-*- encoding:utf-8 -*-

import codecs

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
        # 'LOG_FILE': 'logs/test.log',
        'DOWNLOADER_MIDDLEWARES':{
            # 'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
        }
    }

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.test_page,
            dont_filter=True
        )]

    def test_page(self, response):
        fil = codecs.open('/usr/local/crawler/dxc/I.txt', 'a', encoding='utf-8')
        fil.write('I am I.')
        fil.close()
