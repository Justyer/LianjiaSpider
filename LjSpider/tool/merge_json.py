# import time
# import re
#
# avg_month = '10fhasf'
# if avg_month is None:
#     avg_time = None
# else:
#     y_m = time.strftime("%Y-%m",time.localtime()).split('-')
#     avg_month = re.match(r'\d', avg_month).group(0)
#     print y_m[0], y_m[1]
#     if int(avg_month) > int(y_m[1]):
#         print 'a'
#         print y_m[0] + '-' + avg_month
#     else:
#         print 'b'
#         print str(int(y_m[0]) - 1) + '-' + avg_month
import json
import re
import codecs
# import psycopg2
from collections import OrderedDict
#
# conn = psycopg2.connect(database='ptd', user='postgres', password='495495', host='127.0.0.1', port='5432')
# cur = conn.cursor()
# cur.execute('''
#     select distinct r.id
#     from lj_residence r,lj_community co,lj_district d
#     where r.community_id=co.id and co.district_id=d.id and d.city_id=1
# ''')
# result = cur.fetchall()

fil = codecs.open('lj_esf_all8.json', 'a', encoding='utf-8')
x = 0
for city in ['bj', 'nj', 'cd', 'hf', 'jn', 'qd', 'xm', 'wh']:
    rec = re.compile(r'https://%s' % city)
    f = codecs.open('lj_esf_%s.json' % city, 'r', encoding='utf-8')
    files = [j for j in f]
    for jso in files:
        data = json.loads(jso)
        if rec.findall(data['url']) != []:
            print data['url']
            line = json.dumps(OrderedDict(data), ensure_ascii=False, sort_keys=False) + '\n'
            fil.write(line)
            x += 1

    f.close()
print 'x:', x
fil.close()
    # data['name']
    # data['avg_price']
    # data['avg_time']
    # data['address']
    # data['coordinate']
    # data['build_time']
    # data['property_price']
    # data['property_company']
    # data['developer']
    # data['floor_sum']
    # data['house_sum']
    # data['esf_url']
    # data['deal_url']
    # data['url']
    # data['crawl_time']
    # data['community_id']
