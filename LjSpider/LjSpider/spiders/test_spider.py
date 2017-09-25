#-*- encoding:utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

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

    def __init__(self):
        self.d_c = {}
        d_c_q = Postgresql().query_by_sql('''
            select d.route,c.route,c.id
            from lj_district d,lj_community c
            where d.id=c.district_id
        ''')
        for dc in d_c_q:
            self.d_c[dc[0] + '_' + dc[1]] = dc[2]

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.test_page,
            dont_filter=True
        )]

    def test_page(self, response):
        def rtn(sr):
            try:
                print 'sr front'
                sr
                print 'sr back'
            except:
                return
        no = None
        rtn(no.split('/')[-2])
        # print self.d_c
        # sr = Selector(response)
        # r_district = sr.xpath('//*[@class="fl l-txt"]/a[3]/@href').extract_first().split('/')[-2]
        # r_community = sr.xpath('//*[@class="fl l-txt"]/a[4]/@href').extract_first().split('/')[-2]
        # print r_district + '_' + r_community
        # print self.d_c[r_district + '_' + r_community]
        # print Selector(response).xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span[text()="%s"]/../text()' % u'房屋户型').extract_first()
        # print 'df:::::', Selector(response).xpath('//*[@id="chengjiao_record"]/ul/li[1]/p/text()').extract_first()
        # print 'fasfsd', Selector(response).xpath('//*[@class="msg"]/span[2]/label/text()').extract_first()
        # stre = '   fafs   '
        # print 'front:' + tryex.tryex(stre) + ':back'
        # print Selector(response).xpath('//*[@class="house-title"]/div/span/text()').extract_first().split(' ')
        # sr = Selector(response)
        # print sr.re(r"resblockId:'(.*)'")
        # count = Selector(response).xpath('//*[@class="list-head clear"]/h2/span/text()').extract_first()
        # page = Selector(response).xpath('//*[@gahref="results_totalpage"]/text()').extract_first()
        # print 'count,page:', count, page
        # print response.url + '-------============'
        # page_box = Selector(response).xpath('//*[@class="page-box house-lst-page-box"]').extract_first()
        # if page_box is not None:
        #     totalPage = eval(Selector(text=page_box).xpath('//@page-data').extract_first())['totalPage']
        #     curPage = eval(Selector(text=page_box).xpath('//@page-data').extract_first())['curPage']
        #     if totalPage > curPage:
        #         yield Request(
        #             response.url[0:response.url.find('/', 30) + 1] + 'pg' + str(curPage + 1) + '/',
        #             callback=self.test_page
        #         )
        # sr = Selector(response)
        # print 'result:', sr.xpath('/html/body/div[4]/div/text()').extract_first().split(' ')[0]
        # print 'result:', sr.re(r"resblockName:'[^x00-xff]{1,}'")
        # print Postgresql().query('nice', ['id', 't1', 't2'])
        # print 'headers:', response.headers
        # print 'headers2:', response.request.headers
        # print response.text
        # print Selector(response).xpath('//span[@class="total"]/text()').extract_first()
        # print 'nice:', Selector(text='https://captcha.lianjia.com/').re(r'captcha') == []

        # item = TestItem()
        # item['t1'] = 13
        # item['t2'] = 'rt'
        # print 'type:', type(item)
        # print 'item:', item
        # print isinstance(item, type(item))
        # print 'classname:', item.__class__.__name__
        # print 'name:', item.__table__
        # print 'type_name:', type(item.__table__)
        # print item.__table__ + 'jujuye'
        #
        # Postgresql().insert(item)

        # print 'geta:', Selector(response).xpath('//span[@class="dealTotalPrice"]/i/text()').extract_first()
