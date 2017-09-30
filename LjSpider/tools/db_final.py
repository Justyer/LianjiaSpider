# import psycopg2
#
# conn = psycopg2.connect(database='lj_db', user='postgres', password='495495', host='127.0.0.1', port='5432')
# cur = conn.cursor()

import pymysql.cursors

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='162534',
                       db='dashuju',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
# cur.execute('''
#     create table proxy(
#         id serial primary key,
#         ip varchar(255) not null
#     )
# ''')

# cur.execute('''
#     create table test(
#         id serial primary key,
#         t1 varchar(255) not null,
#         t2 int not null
#     )
# ''')

cur.execute('''
    create table t_web_lj_city(
        id serial primary key,
        cn_name varchar(255) not null,
        route varchar(255) not null,
        url varchar(255) not null
    )
''')

cur.execute('''
    create table t_web_lj_district(
        id serial primary key,
        cn_name varchar(255) not null,
        route varchar(255) not null,
        city_id int not null
    )
''')

cur.execute('''
    create table t_web_lj_community(
        id serial primary key,
        cn_name varchar(255) not null,
        route varchar(255) not null,
        district_id int not null
    )
''')

cur.execute('''
    create table t_web_lj_residence(
        id serial primary key,

        residence_name varchar(255) not null,
        avg_price varchar(255) not null,
        avg_time varchar(255) not null,
        address varchar(255) not null,
        coordinate varchar(255) not null,
        build_time varchar(255) not null,
        property_price varchar(255) not null,
        property_company varchar(255) not null,
        developer varchar(255) not null,
        total_buildings varchar(255) not null,
        total_houses varchar(255) not null,

        bsn_dt varchar(255) not null,
        tms varchar(255) not null,
        url varchar(255) not null,
        webst_nm varchar(255) not null,
        crawl_time varchar(255) not null,
        community_id int not null
    )
''')
#
# cur.execute('''
#     create table lj_residence_around(
#         id serial primary key,
#
#         title varchar(255) not null,
#         description varchar(255) not null,
#         distance varchar(255) not null,
#         type2 varchar(255) not null,
#         type1 varchar(255) not null,
#
#         url varchar(255) not null,
#         crawl_time varchar(255) not null,
#         residence_id int not null
#     )
# ''')
cur.execute('''
    create table t_web_lj_esf(
        id serial primary key,

        structure varchar(255) not null,
        orientation varchar(255) not null,
        area varchar(255) not null,
        inner_area varchar(255) not null,
        heating_style varchar(255) not null,
        decoration varchar(255) not null,
        floor varchar(255) not null,
        total_floor varchar(255) not null,
        house_type_struct varchar(255) not null,
        build_type varchar(255) not null,
        build_struct varchar(255) not null,
        household varchar(255) not null,
        elevator varchar(255) not null,

        ring_num varchar(255) not null,
        lj_num varchar(255) not null,

        house_age varchar(255) not null,
        property_type varchar(255) not null,
        house_type varchar(255) not null,
        house_owner varchar(255) not null,
        listing_date varchar(255) not null,
        total_price varchar(255) not null,
        unit_price varchar(255) not null,
        last_deal varchar(255) not null,
        mortgage varchar(255) not null,
        house_backup varchar(255) not null,

        bsn_dt varchar(255) not null,
        tms varchar(255) not null,
        url varchar(255) not null,
        webbst_nm varchar(255) not null,
        crawl_time varchar(255) not null,
        residence_url varchar(255) not null,
        residence_id int not null
    )
''')

cur.execute('''
    create table t_web_lj_deal(
        id serial primary key,

        structure varchar(255) not null,
        orientation varchar(255) not null,
        area varchar(255) not null,
        inner_area varchar(255) not null,
        heating_style varchar(255) not null,
        decoration varchar(255) not null,
        floor varchar(255) not null,
        total_floor varchar(255) not null,
        house_type_struct varchar(255) not null,
        build_type varchar(255) not null,
        build_struct varchar(255) not null,
        household varchar(255) not null,
        elevator varchar(255) not null,

        house_age varchar(255) not null,
        property_type varchar(255) not null,
        house_type varchar(255) not null,
        house_owner varchar(255) not null,
        listing_price varchar(255) not null,
        listing_date varchar(255) not null,
        total_price varchar(255) not null,
        transaction_date varchar(255) not null,
        last_deal varchar(255) not null,
        deal_cycle varchar(255) not null,
        look_times varchar(255) not null,

        bsn_dt varchar(255) not null,
        tms varchar(255) not null,
        url varchar(255) not null,
        webbst_nm varchar(255) not null,
        crawl_time varchar(255) not null,
        residence_url varchar(255) not null,
        residence_id int not null
    )
''')


print 'db_final ok'
conn.commit()
cur.close()
conn.close()
