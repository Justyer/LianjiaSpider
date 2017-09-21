import datetime
a = '2016.09'
b = '2016.09.20'
d1 = datetime.datetime.strptime(a, '%Y.%M.%d')
d2 = datetime.datetime.strptime(b, '%Y.%M.%d')
print d1, d2
c = d2 - d1
print c.days

# import sys
# sys.path.append("..")
# from LjSpider.Db.Mysql import *
# import fuck

# nice = datetime.datetime.now()
# print nice
# print nice.strftime('%Y-%M-%d')
