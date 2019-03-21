# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HouseDealItem(Item):
    """ house_deal """
    house_id = Field()
    house_url = Field()
    house_title = Field()
    house_dealdate = Field()
    house_dealprice = Field()
    house_perprice = Field()
    house_picturenums = Field()
    house_guapai = Field()
    house_cjterm = Field()
    price_changetimes = Field()
    daikan_times = Field()
    lookatnums = Field()
    views = Field()


class HouseBaseItem(Item):
    """ house_base """
    house_id = Field()
    house_url = Field()
    house_title = Field()
    house_place = Field()
    house_huxin = Field()
    house_floor = Field()
    build_area = Field()
    house_struc = Field()
    taonei_area = Field()
    house_type = Field()
    building_head = Field()
    build_time = Field()
    house_decorate = Field()
    build_struc = Field()
    warm_provide = Field()
    elevator = Field()
    right_year = Field()
    have_elevator = Field()
    lianjia_id = Field()
    deal_right = Field()
    guapai_time = Field()
    house_useway = Field()
    house_rightyear = Field()
    house_right = Field()


class HouseFeatureItem(Item):
    """ house_feature """
    house_id = Field()
    house_tags = Field()
    community_introduce = Field()
    model_introduce = Field()
    tax_parsing = Field()
    sell_point = Field()
    houseowner_cover = Field()
    sell_introduce = Field()
    decorate_describe = Field()
    power_mortgage = Field()
    surround_facility = Field()
    transportation = Field()
    appropriate_crowd = Field()
