# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TestItem(scrapy.Item):
    __table__ = 'test'

    t1 = scrapy.Field()
    t2 = scrapy.Field()

class CityItem(scrapy.Item):
    __table__ = 't_web_lj_city'

    cn_name = scrapy.Field()
    route   = scrapy.Field()
    url     = scrapy.Field()

class DistrictItem(scrapy.Item):
    __table__ = 't_web_lj_district'

    cn_name = scrapy.Field()
    route   = scrapy.Field()
    city_id = scrapy.Field()

class CommunityItem(scrapy.Item):
    __table__ = 't_web_lj_community'

    cn_name     = scrapy.Field()
    route       = scrapy.Field()
    district_id = scrapy.Field()

class ResidenceItem(scrapy.Item):
    __table__ = 't_web_lj_residence'

    residence_name   = scrapy.Field()
    avg_price        = scrapy.Field()
    avg_time         = scrapy.Field()
    address          = scrapy.Field()
    coordinate       = scrapy.Field()
    build_time       = scrapy.Field()
    property_price   = scrapy.Field()
    property_company = scrapy.Field()
    developer        = scrapy.Field()
    total_buildings  = scrapy.Field()
    total_houses     = scrapy.Field()
    bsn_dt           = scrapy.Field()
    tms              = scrapy.Field()
    url              = scrapy.Field()
    webst_nm         = scrapy.Field()
    crawl_time       = scrapy.Field()
    city             = scrapy.Field()
    district         = scrapy.Field()
    community        = scrapy.Field()
    community_id     = scrapy.Field()

# class AroundItem(scrapy.Item):
#     __table__ = 't_web_lj_residence_around'
#
#     title        = scrapy.Field()
#     description  = scrapy.Field()
#     distance     = scrapy.Field()
#     type2        = scrapy.Field()
#     type1        = scrapy.Field()
#     residence_id = scrapy.Field()

class EsfItem(scrapy.Item):
    __table__ = 't_web_lj_esf'

    structure         = scrapy.Field()
    orientation       = scrapy.Field()
    area              = scrapy.Field()
    inner_area        = scrapy.Field()
    heating_style     = scrapy.Field()
    decoration        = scrapy.Field()
    floor             = scrapy.Field()
    total_floor       = scrapy.Field()
    house_type_struct = scrapy.Field()
    build_type        = scrapy.Field()
    build_struct      = scrapy.Field()
    household         = scrapy.Field()
    elevator          = scrapy.Field()

    ring_num          = scrapy.Field()
    lj_num            = scrapy.Field()

    house_age         = scrapy.Field()
    property_type     = scrapy.Field()
    house_type        = scrapy.Field()
    house_owner       = scrapy.Field()
    listing_date      = scrapy.Field()
    total_price       = scrapy.Field()
    unit_price        = scrapy.Field()
    last_deal         = scrapy.Field()
    mortgage          = scrapy.Field()
    house_backup      = scrapy.Field()

    bsn_dt            = scrapy.Field()
    tms               = scrapy.Field()
    url               = scrapy.Field()
    webst_nm          = scrapy.Field()
    crawl_time        = scrapy.Field()
    residence_url     = scrapy.Field()
    residence_id      = scrapy.Field()

# class DealCountItem(scrapy.Item):
#     __table__ = 't_web_lj_deal_count'
#
#     name         = scrapy.Field()
#     count        = scrapy.Field()
#     page         = scrapy.Field()
#     residence_id = scrapy.Field()
#
# class DealNewCountItem(scrapy.Item):
#     __table__ = 't_web_lj_deal_count2_1'
#
#     name         = scrapy.Field()
#     route        = scrapy.Field()
#     count        = scrapy.Field()
#     page         = scrapy.Field()
#     url          = scrapy.Field()
#     community_id = scrapy.Field()

class DealItem(scrapy.Item):
    __table__ = 't_web_lj_deal'

    structure         = scrapy.Field()
    orientation       = scrapy.Field()
    area              = scrapy.Field()
    inner_area        = scrapy.Field()
    heating_style     = scrapy.Field()
    decoration        = scrapy.Field()
    floor             = scrapy.Field()
    total_floor       = scrapy.Field()
    house_type_struct = scrapy.Field()
    build_type        = scrapy.Field()
    build_struct      = scrapy.Field()
    household         = scrapy.Field()
    elevator          = scrapy.Field()

    house_age         = scrapy.Field()
    property_type     = scrapy.Field()
    house_type        = scrapy.Field()
    house_owner       = scrapy.Field()
    listing_date      = scrapy.Field()
    listing_price     = scrapy.Field()
    total_price       = scrapy.Field()
    transaction_date  = scrapy.Field()
    last_deal         = scrapy.Field()
    deal_cycle        = scrapy.Field()
    look_times        = scrapy.Field()

    bsn_dt            = scrapy.Field()
    tms               = scrapy.Field()
    url               = scrapy.Field()
    webst_nm          = scrapy.Field()
    crawl_time        = scrapy.Field()
    residence_url     = scrapy.Field()
    residence_id      = scrapy.Field()
