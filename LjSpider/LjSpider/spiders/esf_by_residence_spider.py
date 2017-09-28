#-*- encoding:utf-8 -*-

import re
import time
import psycopg2

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class EsfByRsdSpider(CrawlSpider):
    name = 'lj_get_esf_rsd'
    start_urls = []
    custom_settings = {
        # 'JOBDIR': 'crawls/lj_get_esf-3',
        # 'LOG_FILE': 'logs/lj_esf_house.log',
        'DOWNLOADER_MIDDLEWARES':{
            'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
            'LjSpider.pipelines.JsonPipeline': 301,
        }
    }

    def start_requests(self):
        # id_esf_url = Postgresql().query('lj_residence', ['id', 'esf_url'])
        id_esf_url = Postgresql().query_by_sql("select id,esf_url from lj_residence where url like 'https://wh.lianjia.com/%'")
        for id_, url in id_esf_url:
            if url != 'None':
                yield Request(
                    url,
                    meta={'id': id_},
                    callback=self.get_esf_url
                )

    def get_esf_url(self,response):
        esf_url = Selector(response).xpath('/html/body/div[4]/div[1]/ul/li/a/@href').extract()

        for url in esf_url:
            yield Request(
                url,
                meta=response.request.meta,
                callback=self.get_esf_info
            )
        page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(Selector(response).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(Selector(response).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                next_page_url = response.url[0:34] + response.url.split('/')[4] + '/' + 'pg' + str(curPage + 1) + '/'
                yield Request(
                    next_page_url,
                    meta=response.request.meta,
                    callback=self.get_esf_url
                )

    def get_esf_info(self, response):
        print 'Url:', response.url

        sr = Selector(response)
        item = EsfItem()
        item['house_type']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()').extract_first()
        item['orientation']       = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[7]/text()').extract_first()
        item['area']              = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()').extract_first()
        item['inner_area']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[5]/text()').extract_first()
        item['heating_style']     = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()').extract_first()
        item['decoration']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()').extract_first()
        item['floor']             = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()').extract_first()
        item['house_type_struct'] = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[4]/text()').extract_first()
        item['build_type']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[6]/text()').extract_first()
        item['build_struct']      = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[8]/text()').extract_first()
        item['household']         = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[10]/text()').extract_first()
        item['elevator']          = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[12]/text()').extract_first()

        item['ring_num']          = sr.xpath('//*[@class="areaName"]/span[2]/text()[2]').extract_first()
        item['lj_num']            = sr.xpath('//*[@class="houseRecord"]/span[2]/text()').extract_first()

        name  = sr.xpath('//*[@class="brokerName"]/a[1]/text()').extract_first()
        phone = sr.xpath('//*[@class="brokerInfoText fr"]/div[3]/text()[1]').extract_first()
        turn  = sr.xpath('//*[@class="brokerInfoText fr"]/div[3]/text()[2]').extract_first()
        try:
            item['broker']        = name + ' ' + phone + ' ' + turn
        except:
            item['broker']        = None

        item['house_age']         = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/text()').extract_first()
        item['transaction_owner'] = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/text()').extract_first()
        item['use']               = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[4]/text()').extract_first()
        item['house_owner']       = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[6]/text()').extract_first()
        item['listing_time']      = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/text()').extract_first()
        item['listing_price']     = sr.xpath('//span[@class="total"]/text()').extract_first()
        item['unit_price']        = sr.xpath('//span[@class="unitPriceValue"]/text()').extract_first()
        item['last_deal']         = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[3]/text()').extract_first()
        item['mortgage']          = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()').extract_first()
        item['house_backup']      = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[8]/text()').extract_first()

        item['url']               = response.url
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())
        item['residence_name']    = sr.xpath('//*[@class="communityName"]/a[1]/text()').extract_first()
        item['residence_id']      = response.request.meta['id']
        yield item
