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

class DealNewSpider(CrawlSpider):
    name = 'lj_get_deal_new'
    start_urls = [
        'https://bj.lianjia.com/chengjiao/',
        'https://lf.lianjia.com/chengjiao/'
    ]
    custom_settings = {
        # 'JOBDIR': 'crawls/lj_get_residence-1',
        'DOWNLOADER_MIDDLEWARES':{
            'LjSpider.middlewares.ProxyMiddleware': 202,
        },
        'ITEM_PIPELINES':{
           'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
        }
    }

    def __init__(self):
        self.website = 'https://bj.lianjia.com/'

    def start_requests(self):
        deal_new = Postgresql().query_by_sql('select d.id,co.route from lj_district as d,lj_community as co where d.id=co.district_id')

        for d_id, route in deal_new:
            if d_id in [18, 19]:
                url = self.start_urls[1]
            else:
                url = self.start_urls[0]
            yield Request(
                url + route + '/',
                callback=self.get_deal_new_url
            )

    def get_deal_new_url(self,response):
        deal_url = Selector(response).xpath('/html/body/div[5]/div[1]/ul/li/a/@href').extract()
        for url in deal_url:
            yield Request(
                url,
                callback=self.get_deal_new_info
            )

        if Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first() is not None:
            totalPage = eval(Selector(response).xpath('//*[@class="page-box house-lst-page-box"]/@page-data').extract_first())['totalPage']
            curPage = eval(Selector(response).xpath('//*[@class="page-box house-lst-page-box"]/@page-data').extract_first())['curPage']
            if totalPage > curPage:
                next_page_url = re.match(r'(https://(bj|lf).lianjia.com/chengjiao/[0-9a-z]{1,})', response.url).group(1)
                yield Request(
                    next_page_url + 'pg' + str(curPage + 1) + '/',
                    callback=self.get_deal_new_url
                )


    def get_deal_new_info(self, response):
        print 'Url:', response.url

        sr = Selector(response)
        item = DealHouseItem()
        item['house_type']        = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[1]/text()').extract_first()
        item['orientation']       = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[7]/text()').extract_first()
        item['area']              = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[3]/text()').extract_first()
        item['inner_area']        = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[5]/text()').extract_first()
        item['heating_style']     = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[11]/text()').extract_first()
        item['decoration']        = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[9]/text()').extract_first()
        item['floor']             = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[2]/text()').extract_first()
        item['house_type_struct'] = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[4]/text()').extract_first()
        item['build_type']        = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[6]/text()').extract_first()
        item['build_struct']      = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[10]/text()').extract_first()
        item['household']         = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[12]/text()').extract_first()
        item['elevator']          = sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[14]/text()').extract_first()
        item['url']               = response.url
        item['create_time']       = time.strftime("%Y-%m-%d %X",time.localtime())
        item['modify_time']       = time.strftime("%Y-%m-%d %X",time.localtime())
        item['residence_name']    = sr.xpath('/html/body/div[4]/div/text()').extract_first().split(' ')[0]
        yield item

        item2 = DealTransactionItem()
        item2['house_age']         = sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li[5]/text()').extract_first()
        item2['transaction_owner'] = sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li[2]/text()').extract_first()
        item2['use']               = sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li[4]/text()').extract_first()
        item2['house_owner']       = sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li[6]/text()').extract_first()
        item2['listing_time']      = sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li[3]/text()').extract_first()
        item2['listing_price']     = sr.xpath('//div[@class="msg"]/span[1]/label/text()').extract_first()
        item2['deal_price']        = sr.xpath('//span[@class="dealTotalPrice"]/i/text()').extract_first()
        item2['last_deal']         = sr.xpath('//*[@id="chengjiao_record"]/ul/li[2]/p/text()').extract_first()
        item2['deal_cycle']        = sr.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[2]/label/text()').extract_first()
        item2['look_times']        = sr.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/span[4]/label/text()').extract_first()
        item2['url']               = response.url
        item2['create_time']       = time.strftime("%Y-%m-%d %X",time.localtime())
        item2['modify_time']       = time.strftime("%Y-%m-%d %X",time.localtime())
        item2['residence_name']    = sr.xpath('/html/body/div[4]/div/text()').extract_first().split(' ')[0]
        yield item2
