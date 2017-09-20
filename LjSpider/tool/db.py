#-*- encoding:utf-8 -*-

import psycopg2

conn = psycopg2.connect(database='ptd', user='postgres', password='495495', host='127.0.0.1', port='5432')
cur = conn.cursor()

# cur.execute('''
#     insert into lj_residence_backup_all(name,avg_price,avg_time,address,coordinate,build_time,property_price,property_company,developer,floor_sum,house_sum,esf_url,deal_url,url,crawl_time,community_id)
#     select name,avg_price,avg_time,address,coordinate,build_time,property_price,property_company,developer,floor_sum,house_sum,esf_url,deal_url,url,crawl_time,community_id from lj_residence
# ''')
cur.execute('''
    select co.id
    from lj_residence r,lj_community co,lj_district d
    where r.community_id=co.id and co.district_id=d.id and d.city_id=1
''')
result = cur.fetchall()
st = '['
for i in result:
    st += str(i[0]) + ", "
print st

print 'db ok'
conn.commit()
cur.close()
conn.close()
