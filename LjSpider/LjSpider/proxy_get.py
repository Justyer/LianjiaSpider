import requests
import codecs
import time

from Db.Postgresql import *

while True:
    try:
        url = 'http://http-webapi.zhimaruanjian.com/getip?num=1&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1'
        proxy_url = requests.get(url=url,timeout=2).text.strip()
        Postgresql().insert_by_sql("update proxy set ip='%s' where id=1" % proxy_url)
        print 'proxyUrl:', proxy_url
        time.sleep(180)
    except Exception, e:
        print 'proxy error!!!'
        print e
