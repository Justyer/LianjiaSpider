import pymysql.cursors

class Mysql(object):

    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='162534',
                                    db='dashuju',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()

    def insert_by_item(self, item):
        try:
            key, value = ('', '')
            for k in item.keys():
                key += ',' + k
                if isinstance(item[k], int):
                    value += ',' + str(item[k])
                else:
                    if item[k] is None:
                        item[k] = 'null'
                        value += "," + item[k]
                    else:
                        value += ",'" + item[k] + "'"
            sql = 'insert into ' + item.__table__ + '(' + key[1:] + ') ' + 'values(' + value[1:] + ')'
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print '[' + item.__table__ + '] insert failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

    def insert_by_dict(self, table_name, dict_):
        try:
            key, value = ('', '')
            for k in dict_.keys():
                key += ',' + k
                if isinstance(dict_[k], int):
                    value += ',' + str(dict_[k])
                else:
                    if dict_[k] is None:
                        dict_[k] = 'null'
                        value += "," + dict_[k]
                    else:
                        value += ",'" + dict_[k] + "'"
            sql = 'insert into ' + table_name + '(' + key[1:] + ') ' + 'values(' + value[1:] + ')'
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print '[' + table_name + '] insert failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

    def insert_by_sql(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print '[' + sql + '] insert failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

    def insert_return_id(self, item):
        try:
            key, value = ('', '')
            for k in item.keys():
                key += ',' + k
                if isinstance(item[k], int):
                    value += ',' + str(item[k])
                else:
                    value += ",'" + item[k] + "'"
            sql = 'insert into ' + item.__table__ + '(' + key[1:] + ') ' + 'values(' + value[1:] + ') returning id'
            self.cur.execute(sql)
            return_id = self.cur.fetchone()[0]
            self.conn.commit()
            return return_id
        except Exception, e:
            print '[' + item.__table__ + '] insert_return_id failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

    def query_one(self, table_name, query_rows):
        try:
            query = ''
            for qr in query_rows:
                query += ',' + qr
            sql = 'select ' + query[1:] + ' from ' + table_name
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception, e:
            print '[' + table_name + '] query_one failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

    def query(self, table_name, query_rows):
        try:
            query = ''
            for qr in query_rows:
                query += ',' + qr
            sql = 'select ' + query[1:] + ' from ' + table_name
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception, e:
            print '[' + table_name + '] query failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

    def query_by_sql(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception, e:
            print '[' + sql + '] query failed:' + str(e)
        finally:
            self.cur.close()
            self.conn.close()

if __name__ == '__main__':
    m = Mysql()
    print m.insert_by_sql("insert into nice(ip) values('zuole')")
    # print m.insert_by_sql("delete from nice where ip='zuole'")
    # print result
