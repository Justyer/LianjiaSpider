#-*- encoding:utf-8 -*-

# import datetime
# a = '2016.09.18'
# b = '2016.09.20'
# d1 = datetime.datetime.strptime(a, '%Y.%M.%d')
# d2 = datetime.datetime.strptime(b, '%Y.%M.%d')
# print d1, d2, type(d1), type(d2)
# c = d2 - d1
# print c.days

# import sys
# sys.path.append("..")
# from LjSpider.Db.Mysql import *
# import fuck

# nice = datetime.datetime.now()
# print nice
# print nice.strftime('%Y-%M-%d')

# def fu():
#     try:
#         nice = datetime.days
#     except:
#         return 'wocuole'
#     return 'womeicuo'
#
# print fu()
# import datetime
# today = datetime.date.today()
# oneday = datetime.timedelta(days=1)
# yesterday = today - oneday
# # print type(str(yesterday))
#
# old_latest_date = datetime.datetime.strptime(str(yesterday), '%Y-%m-%d')
# latest_date = datetime.datetime.strptime('2017.09.22', '%Y.%m.%d')
# day_space = (latest_date - old_latest_date).days
# print old_latest_date, latest_date, day_space

# import csv
# import codecs
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
#
# csv_reader = csv.DictReader(codecs.open('../esf_irt_20170922.csv', 'r', encoding='utf-8'))
# for row in csv_reader:
#     print 'f:', row['residence_url']
fabu_time_tian = ['0']
if fabu_time_tian != [] and (int(fabu_time_tian[0]) == 0 or int(fabu_time_tian[0]) > 1):
    print 'return'
else:
    print 'resume'
