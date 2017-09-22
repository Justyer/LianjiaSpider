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
from LjSpider.Exception import tryex

class DealSpider(CrawlSpider):
    name = 'lj_get_deal'
    start_urls = []
    custom_settings = {
        'JOBDIR': 'crawls/lj_get_deal-njaby',
        # 'LOG_FILE': 'logs/lj_esf_transaction.log',
        'DOWNLOADER_MIDDLEWARES':{
            # 'LjSpider.middlewares.ProxyMiddleware': 202,
            'LjSpider.middlewares.ProxyABYMiddleware': 203,
        },
        'ITEM_PIPELINES':{
        #    'LjSpider.pipelines.InsertPostgresqlPipeline': 300,
            # 'LjSpider.pipelines.JsonPipeline': 300,
        }
    }

    def start_requests(self):
        id_route = Postgresql().query_by_sql('''
                        select co.route,c.url
                        from lj_district d,lj_community co,lj_city c
                        where d.id=co.district_id and d.city_id=c.id
                    ''')
        for route, url in id_route:
            yield Request(
                url + 'chengjiao/' + route + '/',
                callback=self.get_deal_url,
                dont_filter=True
            )

    def get_deal_url(self,response):
        deal_url = Selector(response).xpath('/html/body/div[5]/div[1]/ul/li/a/@href').extract()
        for url in deal_url:
            yield Request(
                url,
                callback=self.get_deal_info,
                dont_filter=True
            )

        page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(Selector(response).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(Selector(response).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                next_page_url = response.url[0:33] + response.url.split('/')[4] + '/' + 'pg' + str(curPage + 1) + '/'
                yield Request(
                    next_page_url,
                    callback=self.get_deal_url,
                    dont_filter=True
                )

    def get_deal_info(self, response):
        print 'Url:', response.url

        sr = Selector(response)
        item = DealItem()

        item['structure']         = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋户型').extract_first())
        item['orientation']       = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋朝向').extract_first())
        item['area']              = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑面积').extract_first())
        item['inner_area']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'套内面积').extract_first())
        item['heating_style']     = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'供暖方式').extract_first())
        item['decoration']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'装修情况').extract_first())

        rec = re.compile(r'\d+')
        fl = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'所在楼层').extract_first()).split(' ')
    	if len(fl) == 2:
    		item['floor'] = fl[0]
    		item['total_floor'] = rec.findall(fl[1])[0]
        else:
    		item['floor'] = None
    		item['total_floor'] = None

        item['house_type_struct'] = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'户型结构').extract_first())
        item['build_type']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑类型').extract_first())
        item['build_struct']      = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑结构').extract_first())
        item['household']         = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'梯户比例').extract_first())
        item['elevator']          = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'配备电梯').extract_first())

        item['house_age']         = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋年限').extract_first())
        item['property_type']     = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'交易权属').extract_first())
        item['house_type']        = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋用途').extract_first())
        item['house_owner']       = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房权所属').extract_first())
        item['listing_date']      = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'挂牌时间').extract_first())
        item['listing_price']     = tryex.strip(sr.xpath('//div[@class="msg"]/span[1]/label/text()').extract_first())
        item['total_price']       = tryex.strip(sr.xpath('//span[@class="dealTotalPrice"]/i/text()').extract_first())

        transaction_date = tryex.strip(sr.xpath('//*[@class="house-title"]/div/span/text()').extract_first())
        if transaction_date:
            item['transaction_date'] = transaction_date.split(' ')[0]
        else:
            item['transaction_date'] = None

        item['last_deal']         = tryex.strip(sr.xpath('//*[@id="chengjiao_record"]/ul/li[2]/p/text()').extract_first())
        item['deal_cycle']        = tryex.strip(sr.xpath('//*[@class="msg"]/span[2]/label/text()').extract_first())
        item['look_times']        = tryex.strip(sr.xpath('//*[@class="msg"]/span[4]/label/text()').extract_first())

        item['url']               = response.url
        item['crawl_time']        = time.strftime("%Y-%m-%d %X",time.localtime())
        item['residence_url']     = response.url[0:23]+ 'xiaoqu/' + sr.re(r"resblockId:'(.*)'")[0] + '/'
        item['residence_id']      = -3
        yield item
