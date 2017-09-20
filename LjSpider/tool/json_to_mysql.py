#-*- encoding:utf-8 -*-

import codecs
import json
import re
import time
from datetime import datetime
from collections import OrderedDict

import sys
sys.path.append("..")
from LjSpider.Db.Postgresql import *
from LjSpider.Db.Mysql import *
# import psycopg2
# import pymysql.cursors

# pg_conn = psycopg2.connect(host='localhost',
# 								 user='root',
# 								 password='495495',
# 								 database='ptd')
# pg_cur = pg_conn.cursor()

# my_conn = pymysql.connect(host='localhost',
#                        user='root',
#                        password='162534',
#                        db='dashuju',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)
# my_cur = my_conn.cursor()
start_time = datetime.now()
print 'start_time:', start_time
# f = codecs.open('xcodde.json', 'a', encoding='utf-8')
rec = re.compile(r'\d+')
fil = codecs.open('lj_esf_all8.json', 'r', encoding='utf-8')
files = [j for j in fil]
for jso in files:
	data = json.loads(jso)
	dct = {}
	dct['structure'] = data['structure']
	dct['orientation'] = data['orientation']
	dct['area'] = data['area']
	dct['inner_area'] = data['inner_area']
	dct['heating_style'] = data['heating_style']
	dct['decoration'] = data['decoration']

	f_tf = data['floor'].split(' ')
	if len(f_tf) == 2:
		dct['floor'] = f_tf[0]
		dct['total_floor'] = rec.findall(f_tf[1])[0]

	dct['house_type_struct'] = data['house_type_struct']
	dct['build_type'] = data['build_type']
	dct['build_struct'] = data['build_struct']
	dct['household'] = data['household']
	dct['elevator'] = data['elevator']

	dct['ring_num'] = data['ring_num']
	dct['lj_num'] = data['lj_num']

	dct['house_age'] = data['house_age']
	dct['property_type'] = data['property_type']
	dct['house_type'] = data['house_type']
	dct['house_owner'] = data['house_owner']
	dct['listing_date'] = data['listing_date']
	dct['total_price'] = data['total_price']
	dct['unit_price'] = data['unit_price']
	dct['last_deal'] = data['last_deal']
	dct['mortgage'] = data['mortgage']
	dct['house_backup'] = data['house_backup']

	dct['bsn_dt'] = None
	dct['tms'] = time.strftime("%Y-%m-%d %X",time.localtime())
	dct['url'] = data['url']
	dct['webbst_nm'] = u'链家'
	dct['crawl_time'] = data['crawl_time']
	dct['residence_url'] = None
	dct['residence_id'] = data['residence_id']
	# line = json.dumps(OrderedDict(dct), ensure_ascii=False, sort_keys=False) + '\n'
	# f.write(line)
	# break
	Mysql().insert_by_dict('t_web_lj_esf', dct)

end_time = datetime.now()
print 'end_time:', end_time

print 'seconds:', (end_time - start_time).seconds