import psycopg2

conn = psycopg2.connect(database='ptd', user='postgres', password='495495', host='127.0.0.1', port='5432')
cur = conn.cursor()

cur.execute('''
    create table proxy(
        id serial primary key,
        ip varchar(255) not null
    )
''')

# cur.execute('''
#     create table test(
#         id serial primary key,
#         t1 varchar(255) not null,
#         t2 bigint not null
#     )
# ''')

# cur.execute('''
#     create table lj_city(
#         id serial primary key,
#         cn_name varchar(255) not null,
#         route varchar(255) not null,
#         url varchar(255) not null
#     )
# ''')
#
# cur.execute('''
#     create table lj_district(
#         id serial primary key,
#         cn_name varchar(255) not null,
#         route varchar(255) not null,
#         city_id bigint not null
#     )
# ''')

# cur.execute('''
#     create table lj_community(
#         id serial primary key,
#         cn_name varchar(255) not null,
#         route varchar(255) not null,
#         district_id bigint not null
#     )
# ''')

# cur.execute('''
#     create table lj_residence(
#         id serial primary key,
#
#         name varchar(255) not null,
#         avg_price varchar(255) not null,
#         avg_time varchar(255) not null,
#         address varchar(255) not null,
#         coordinate varchar(255) not null,
#         build_time varchar(255) not null,
#         property_price varchar(255) not null,
#         property_company varchar(255) not null,
#         developer varchar(255) not null,
#         floor_sum varchar(255) not null,
#         house_sum varchar(255) not null,
#
#         esf_url varchar(255) not null,
#         deal_url varchar(255) not null,
#         url varchar(255) not null,
#         crawl_time varchar(255) not null,
#         community_id bigint not null
#     )
# ''')
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
#         residence_id bigint not null
#     )
# ''')
# cur.execute('''
#     create table lj_esf(
#         id serial primary key,
#
#         house_type varchar(255) not null,
#         orientation varchar(255) not null,
#         area varchar(255) not null,
#         inner_area varchar(255) not null,
#         heating_style varchar(255) not null,
#         decoration varchar(255) not null,
#         floor varchar(255) not null,
#         house_type_struct varchar(255) not null,
#         build_type varchar(255) not null,
#         build_struct varchar(255) not null,
#         household varchar(255) not null,
#         elevator varchar(255) not null,
#
#         ring_num varchar(255) not null,
#         lj_num varchar(255) not null,
#         broker varchar(255) not null,
#
#         house_age varchar(255) not null,
#         transaction_owner varchar(255) not null,
#         use varchar(255) not null,
#         house_owner varchar(255) not null,
#         listing_time varchar(255) not null,
#         listing_price varchar(255) not null,
#         unit_price varchar(255) not null,
#         last_deal varchar(255) not null,
#         mortgage varchar(255) not null,
#         house_backup varchar(255) not null,
#
#         url varchar(255) not null,
#         crawl_time varchar(255) not null,
#         residence_name varchar(255) not null,
#         residence_id bigint not null
#     )
# ''')
#
# cur.execute('''
#     create table lj_deal(
#         id serial primary key,
#
#         house_type varchar(255) not null,
#         orientation varchar(255) not null,
#         area varchar(255) not null,
#         inner_area varchar(255) not null,
#         heating_style varchar(255) not null,
#         decoration varchar(255) not null,
#         floor varchar(255) not null,
#         house_type_struct varchar(255) not null,
#         build_type varchar(255) not null,
#         build_struct varchar(255) not null,
#         household varchar(255) not null,
#         elevator varchar(255) not null,
#
#         house_age varchar(255) not null,
#         transaction_owner varchar(255) not null,
#         use varchar(255) not null,
#         house_owner varchar(255) not null,
#         listing_time varchar(255) not null,
#         listing_price varchar(255) not null,
#         deal_price varchar(255) not null,
#         deal_time varchar(255) not null,
#         last_deal varchar(255) not null,
#         deal_cycle varchar(255) not null,
#         look_times varchar(255) not null,
#
#         url varchar(255) not null,
#         crawl_time varchar(255) not null,
#         residence_url varchar(255) not null,
#         residence_id bigint not null,
#
#     )
# ''')


print 'db_new ok'
conn.commit()
cur.close()
conn.close()
