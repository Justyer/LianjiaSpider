#-*- encoding:utf-8 -*-

import re
import psycopg2
import datetime

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Mysql import *
from LjSpider.Exception import tryex

class EsfIrtSpider(CrawlSpider):
    name = 'lj_get_esf_irt'
    start_urls = []
    custom_settings = {
        'FEED_URI': '/usr/local/crawler/dxc/common/lj/data/lj_esf_irt_%s.csv' % datetime.date.today(),
        'JOBDIR': '/usr/local/crawler/dxc/common/lj/crawls/lj_esf_irt_%s' % datetime.date.today(),
        'LOG_FILE': '/usr/local/crawler/dxc/common/lj/logs/lj_esf_irt_%s.log' % datetime.date.today(),
        'DOWNLOADER_MIDDLEWARES':{
            'LjSpider.middlewares.ProxyMiddleware': 202,
            # 'LjSpider.middlewares.ProxyxxxMiddleware': 302,
        },
        'ITEM_PIPELINES':{
           'LjSpider.pipelines.InsertMysqlPipeline': 300,
            # 'LjSpider.pipelines.JsonHFPipeline': 301,
        }
    }

    def start_requests(self):
        id_esf_url = Mysql().query_by_sql('''
                        select co.route,c.url
                        from t_web_lj_community co,t_web_lj_district d,t_web_lj_city c
                        where d.id=co.district_id and d.city_id=c.id
                    ''')
        for route_url in id_esf_url:
            yield Request(
                route_url['url'] + 'ershoufang/' + route_url['route'] + '/co32/',
                callback=self.get_esf_url,
                dont_filter=True
            )
        # return [Request(
        #     'https://nj.lianjia.com/ershoufang/hanzhongmendajie/co32/',
        #     callback=self.get_esf_url,
        #     dont_filter=True
        # )]

    def get_esf_url(self,response):
        into_it = Selector(response).xpath('/html/body/div[4]/div[1]/ul/li[1]/div[1]/div[4]/text()').extract_first()
        if not into_it:
            return
        fabu_time_gang = Selector(text=into_it).re(r'%s' % u'刚刚发布')
        fabu_time_tian = Selector(text=into_it).re(r'(\d+)%s' % u'天以前发布')
        print fabu_time_gang, fabu_time_tian
        if not fabu_time_gang and not fabu_time_tian:
            return
        if fabu_time_tian != [] and (int(fabu_time_tian[0]) == 0 or int(fabu_time_tian[0]) > 1):
            return

        esf_url = Selector(response).xpath('/html/body/div[4]/div[1]/ul/li/a/@href').extract()
        for url in esf_url:
            yield Request(
                url,
                meta=response.request.meta,
                callback=self.get_esf_info,
                dont_filter=True
            )
        page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(Selector(response).xpath('//@page-data').extract_first())['totalPage']
            curPage = eval(Selector(response).xpath('//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                yield Request(
                    response.url[0:response.url.find('/', 34) + 1] + 'pg' + str(curPage + 1) + 'co32/',
                    meta=response.request.meta,
                    callback=self.get_esf_url,
                    dont_filter=True
                )

    def get_esf_info(self, response):
        # print 'Url:', response.url

        sr = Selector(response)
        item = EsfItem()

        listing_date = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'挂牌时间').extract_first()
        today = datetime.date.today()
        oneday = datetime.timedelta(days=3)
        yesterday = today - oneday
        old_latest_date = datetime.datetime.strptime(str(yesterday), '%Y-%m-%d')
        try:
            latest_date = datetime.datetime.strptime(listing_date, '%Y-%m-%d')
        except:
            return
        day_space = (latest_date - old_latest_date).days
        if day_space < 0:
            return

        item['structure']         = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋户型').extract_first()
        item['orientation']       = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋朝向').extract_first()
        item['area']              = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑面积').extract_first()
        item['inner_area']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'套内面积').extract_first()
        item['heating_style']     = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'供暖方式').extract_first()
        item['decoration']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'装修情况').extract_first()

        rec = re.compile(r'\d+')
        fl = tryex.strip(sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'所在楼层').extract_first()).split(' ')
    	if len(fl) == 2:
    		item['floor'] = fl[0]
    		item['total_floor'] = rec.findall(fl[1])[0]
        else:
    		item['floor'] = None
    		item['total_floor'] = None

        item['house_type_struct'] = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'户型结构').extract_first()
        item['build_type']        = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑类型').extract_first()
        item['build_struct']      = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'建筑结构').extract_first()
        item['household']         = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'梯户比例').extract_first()
        item['elevator']          = sr.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'配备电梯').extract_first()

        item['ring_num']          = sr.xpath('//*[@class="areaName"]/span[2]/text()[2]').extract_first()
        item['lj_num']            = sr.xpath('//*[@class="houseRecord"]/span[2]/text()').extract_first()

        item['house_age']         = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋年限').extract_first()
        item['property_type']     = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'交易权属').extract_first()
        item['house_type']        = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋用途').extract_first()
        item['house_owner']       = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'产权所属').extract_first()
        item['listing_date']      = listing_date
        item['total_price']       = sr.xpath('//span[@class="total"]/text()').extract_first()
        item['unit_price']        = sr.xpath('//span[@class="unitPriceValue"]/text()').extract_first()
        item['last_deal']         = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'上次交易').extract_first()
        item['mortgage']          = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../span[2]/text()' % u'抵押信息').extract_first()
        item['house_backup']      = sr.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房本备件').extract_first()

        item['bsn_dt']            = str(datetime.date.today())
        item['tms']               = datetime.datetime.now().strftime('%Y-%m-%d %X')
        item['url']               = response.url
        item['webst_nm']          = u'链家'
        item['crawl_time']        = datetime.datetime.now().strftime('%Y-%m-%d %X')

        residence_url = sr.xpath('//*[@class="communityName"]/a[1]/@href').extract_first()
        if residence_url is not None:
            item['residence_url'] = response.url[0:22] + residence_url
        else:
            item['residence_url'] = sr.xpath('//*[@class="communityName"]/a[1]/text()').extract_first()
        item['residence_id']      = 0
        yield item
