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
        'https://qd.lianjia.com/xiaoqu/shinan/',
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
            meta={'first': 'woshi1'},
            callback=self.test_page,
            dont_filter=True
        )]

    def test_page(self, response):
        li = Selector(response).xpath('/html/body/div[4]/div[1]/ul/li').extract()
        for l in li:
            st        = Selector(text=l)
            url       = st.xpath('//*[@class="img"]/@href').extract_first()
            district  = st.xpath('//*[@class="district"]/text()').extract_first()
            community = st.xpath('//*[@class="bizcircle"]/text()').extract_first()
            print 'fnsl:', district, community
        yield Request(
            'https://qd.lianjia.com/xiaoqu/1511041269006/',
            meta={'second': 'woshi2'},
            callback=self.test_info
        )

    def test_info(self, response):
        print 'meta:', response.request.meta
