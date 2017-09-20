# -*- coding: utf-8 -*-

import scrapy
import psycopg2
import codecs
import json

from collections import OrderedDict

from LjSpider.items import *
from LjSpider.Db.Postgresql import *

class InsertPostgresqlPipeline(object):
    def process_item(self, item, spider):
        Postgresql().insert_by_item(item)
        return item

class JsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('sh_re.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = ''
        line += json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + '\n'
        self.file.write(line)
        return item

class Json2Pipeline(object):

    def __init__(self):
        self.file = codecs.open('esf_10000_20000_new.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = ''
        line += json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + '\n'
        self.file.write(line)
        return item

class Json3Pipeline(object):

    def __init__(self):
        self.file = codecs.open('esf_20000_30000_new.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = ''
        line += json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + '\n'
        self.file.write(line)
        return item

class JsonHFPipeline(object):

    def __init__(self):
        self.file = codecs.open('esf_HF2.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = ''
        line += json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + '\n'
        self.file.write(line)
        return item
