# -*- coding: utf-8 -*-

import time
import logging as log
import random
import re
import psycopg2
import requests
import base64

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from commondata import xre, type12

from LjSpider.Db.Postgresql import *

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            url = 'http://api.ip.data5u.com/dynamic/get.html?order=82fdbca90fb003889c47a3bfc3d5897c&sep=5'
            proxy_url = requests.get(url=url,timeout=2).text.split(',')[0]
            print 'proxyUrl:', proxy_url
            if proxy_url != 'too many requests' and proxy_url[0] != '{':
                request.meta['proxy'] = "http://" + proxy_url
        except Exception, e:
            pass

class ProxyZMiddleware(object):
    def process_request(self, request, spider):
        try:
            f = codecs.open('proxy_url.txt', 'r', encoding='utf-8')
            proxy_url = f.read()
            print 'proxyUrl:', proxy_url
            if proxy_url != "":
                request.meta['proxy'] = "http://" + proxy_url
        except Exception, e:
            print 'my ip>>>'
        finally:
            if f is not None:
                f.close()

class ProxyZPMiddleware(object):
    def process_request(self, request, spider):
        try:
            proxy_url = Postgresql().query_by_sql('select ip from proxy where id=1')[0][0]
            print 'proxyUrl:', proxy_url
            if proxy_url is not None:
                request.meta['proxy'] = "http://" + proxy_url
        except Exception, e:
            print 'my ip>>>'

class ProxyABYMiddleware(object):
        def __init__(self):
            self.proxyServer = "http://http-dyn.abuyun.com:9020"
            self.proxyUser = "HRW6D00S2278PQ5D"
            self.proxyPass = "78E5B06B46D6727D"
            self.proxyAuth = "Basic " + base64.b64encode(self.proxyUser + ":" + self.proxyPass)
        def process_request(self, request, spider):
            request.meta["proxy"] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth

class ProxyxxxMiddleware(object):
        def __init__(self):
            self.proxyServer = "http://http-dyn.abuyun.com:9020"
            self.proxyUser = "H604ORTSP1475H4D"
            self.proxyPass = "49DAEF87B1EB5A4F"
            self.proxyAuth = "Basic " + base64.b64encode(self.proxyUser + ":" + self.proxyPass)
        def process_request(self, request, spider):
            request.meta["proxy"] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth

# class BlockCaptchaMiddleware(object):
#     def process_request(self, request, spider):
#         if Selector(text=request.url).re(r'captcha') == []:
#             pass

# class AroundMiddleware(object):
#     def process_request(self, request, spider):
#         if re.match(r'(https://(bj|lf).lianjia.com/xiaoqu/[0-9]{13,}/)', request.url) is not None:
#             print 'currentUrl:', request.url
#             # driver = webdriver.Chrome()
#             dcap = dict(DesiredCapabilities.PHANTOMJS)
#             dcap["phantomjs.page.settings.userAgent"] = (
#             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
#             )
#             driver = webdriver.PhantomJS(desired_capabilities=dcap)
#             driver.maximize_window()
#             #driver.set_window_size(800, 300)
#             # driver.set_page_load_timeout(10)
#             driver.implicitly_wait(30)
#             driver.get(request.url)
#
#             request.meta['around'] = []
#             body = driver.page_source
#
#             for x, t in zip(xre, type12):
#                 pr = driver.find_element_by_xpath('//*[@id="mapListContainer"]').get_attribute('innerHTML')
#                 sr = Selector(text=pr)
#                 title = sr.xpath('//span[@class="itemText itemTitle"]/text()').extract()
#                 description = sr.xpath('//div[@class="itemInfo"]/text()').extract()
#                 distance = sr.xpath('//span[@class="itemText itemdistance"]/text()').extract()
#                 for ti, di, de in zip(title, distance, description):
#                     request.meta['around'].append({'title': ti, 'description': de, 'distance': di, 'type2': t[1], 'type1': t[0]})
#                 elem = driver.find_element_by_xpath(x)
#                 ActionChains(driver).click(elem).perform()
#                 time.sleep(0.01)
#             driver.close()
#             return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
