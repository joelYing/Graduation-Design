# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from LianJia.items import HouseDealItem, HouseBaseItem, HouseFeatureItem


class LianJiaHousePipeline(object):
    def __init__(self, dbpool):
        self.db_pool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor,  # 指定cursor类型
            charset='utf8'
        )

        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)

        # 返回实例化参数
        return cls(dbpool)

    def close_spider(self, spider):
        self.db_pool.close()

    def process_item(self, item, spider):
        """ 判断item的类型"""
        if isinstance(item, HouseDealItem):
            self.db_pool.runInteraction(self.insert_deal_item, item)

        elif isinstance(item, HouseBaseItem):
            self.db_pool.runInteraction(self.insert_base_item, item)

        elif isinstance(item, HouseFeatureItem):
            self.db_pool.runInteraction(self.insert_feature_item, item)

        return item

    def insert_deal_item(self, cursor, item):
        insert_sql = "insert into `house_deal` (`house_id`, `house_url`, `house_title`, `house_dealdate`, " \
                     "`house_dealprice`, `house_perprice`, `house_picturenums`, `house_guapai`, `house_cjterm`, " \
                     "`price_changetimes`, `daikan_times`, `lookatnums`, `views`) values " \
                     "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (item['house_id'],
                                                                                             item['house_url'],
                                                                                             item['house_title'],
                                                                                             item['house_dealdate'],
                                                                                             item['house_dealprice'],
                                                                                             item['house_perprice'],
                                                                                             item['house_picturenums'],
                                                                                             item['house_guapai'],
                                                                                             item['house_cjterm'],
                                                                                             item['price_changetimes'],
                                                                                             item['daikan_times'],
                                                                                             item['lookatnums'],
                                                                                             item['views'])
        select_sql = "select `house_id` from `house_deal` where `house_id`='%s'" % item['house_id']
        result = cursor.execute(select_sql)
        if result == 1:
            print(u'该房源deal已存在')
        else:
            cursor.execute(insert_sql)
            print(u'房源deal插入成功')

    def insert_base_item(self, cursor, item):
        insert_sql = "insert into `house_base` (`house_id`, `house_url`, `house_title`, `house_place`, `house_huxin`, " \
                     "`house_floor`, `build_area`, `house_struc`, `taonei_area`, `house_type`, `building_head`, " \
                     "`build_time`, `house_decorate`,  `build_struc`, `warm_provide`, `elevator`, `right_year`, " \
                     "`have_elevator`, `lianjia_id`, `deal_right`, `guapai_time`, `house_useway`, `house_rightyear`, " \
                     "`house_right`)values" \
                     "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                     "'%s','%s','%s','%s','%s','%s')" % (item['house_id'], item['house_url'],
                                                         item['house_title'], item['house_place'],
                                                         item['house_huxin'], item['house_floor'],
                                                         item['build_area'], item['house_struc'],
                                                         item['taonei_area'], item['house_type'],
                                                         item['building_head'], item['build_time'],
                                                         item['house_decorate'], item['build_struc'],
                                                         item['warm_provide'], item['elevator'],
                                                         item['right_year'], item['have_elevator'],
                                                         item['lianjia_id'], item['deal_right'],
                                                         item['guapai_time'], item['house_useway'],
                                                         item['house_rightyear'], item['house_right'])
        select_sql = "select `house_id` from `house_base` where `house_id`='%s'" % item['house_id']
        result = cursor.execute(select_sql)
        if result == 1:
            print(u'该房源base已存在')
        else:
            cursor.execute(insert_sql)
            print(u'房源base插入成功')

    def insert_feature_item(self, cursor, item):
        insert_sql = "insert into `house_feature` (`house_id`, `house_tags`, `community_introduce`, `model_introduce`" \
                     ", `tax_parsing`, `sell_point`, `houseowner_cover`, `sell_introduce`, `decorate_describe`, " \
                     "`power_mortgage`, `surround_facility`, `transportation`, `appropriate_crowd`)values" \
                     "('%s','%s','%s','%s','%s','%s','%s','%s'," \
                     "'%s','%s','%s','%s','%s')" % (item['house_id'], item['house_tags'],
                                                    item['community_introduce'], item['model_introduce'],
                                                    item['tax_parsing'], item['sell_point'],
                                                    item['houseowner_cover'],
                                                    item['sell_introduce'], item['decorate_describe'],
                                                    item['power_mortgage'], item['surround_facility'],
                                                    item['transportation'],
                                                    item['appropriate_crowd'])
        select_sql = "select `house_id` from `house_feature` where `house_id`='%s'" % item['house_id']
        result = cursor.execute(select_sql)
        if result == 1:
            print(u'该房源feature已存在')
        else:
            cursor.execute(insert_sql)
            print(u'房源feature插入成功')

    @staticmethod
    def handle_error(failure):
        if failure:
            # 打印错误信息
            print(failure)
