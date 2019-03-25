#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:joel
# time:2019/3/14 13:05

import math
import pymysql
import requests
import re
from lxml import etree


"""
北京 成交二手房 790980 小区个数 11638 在售二手房...
上海 成交二手房 164075 小区个数 31205 在售二手房...
广州 成交二手房 27028  小区个数 8732  在售二手房...
深圳 成交二手房 78324  小区个数 6517  在售二手房...
杭州 成交二手房 30423  小区个数 5936  在售二手房...

目前只能遍历出最多 3000 个小区
"""


class LianJia():
    def __init__(self):
        # self.village_area = {'bj': '北京', 'sh': '上海', 'gz': '广州', 'sz': '深圳', 'hz': '杭州'}
        self.village_area = {'sh': '上海', 'gz': '广州', 'sz': '深圳', 'hz': '杭州'}
        self.cj_list = []
        # 11633 个小区 388页 一页30个
        self.xiaoqu_list = "https://{}.lianjia.com/xiaoqu/pg{}/"   # 2993 默认排序
        self.xiaoqu_list_cro11 = "https://{}.lianjia.com/xiaoqu/pg{}cro11/"  # 按成交量
        self.xiaoqu_list_cro21 = "https://{}.lianjia.com/xiaoqu/pg{}cro21/"  # 小区均价
        self.xq_list_search_ways = [self.xiaoqu_list, self.xiaoqu_list_cro11, self.xiaoqu_list_cro21]
        # 遍历以上三个链接，100页之后都一样
        self.xiaoqu_cj_list = "https://bj.lianjia.com/chengjiao/pg{}c{}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }

    def get_xiaoqu_url(self):
        s = requests.session()
        for area in self.village_area.keys():
            for way in self.xq_list_search_ways:
                for xq_page in range(1, 102):
                    print(xq_page)
                    r1 = s.get(way.format(area, xq_page), headers=self.headers)
                    # print(r1.text)
                    xq_url_list = re.findall(r'<li class="clear xiaoquListItem".*?<a class="img" href="(.*?)".*?>'
                                             r'.*?<img class="lj-lazy".*?alt="(.*?)">.*?<a title=".*?网签"  href='
                                             r'"(.*?)".*?>.*?</li>', r1.text, re.S)
                    for xq in xq_url_list:
                        xq_url = xq[0]
                        xq_id = re.sub('https://{}\.lianjia\.com/xiaoqu/|/'.format(area), '', xq_url)
                        xq_name = xq[1]
                        xq_cj_url = xq[2]
                        xq_place = self.village_area[area]
                        print(xq_id, xq_url, xq_name, xq_cj_url)
                        self.insert(xq_id, xq_url, xq_name, xq_cj_url, xq_place)
                    # break

    def w_cj(self):
        with open("D:\\pyprogram\\LianJia\\cj_urls.txt", 'w') as fw:
            for cjurl in self.cj_list:
                fw.writelines(cjurl + '\n')

    def insert(self, xq_id, xq_url, xq_name, xq_cj_url, xq_place):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianjia')
        cursor = conn.cursor()

        insert_sql = "insert into `xq_copy` (`xq_id`, `xq_url`, `xq_name`, `xq_cj_url`, `xq_place`)values" \
                     "('%s','%s','%s','%s','%s')" % (xq_id, xq_url, xq_name, xq_cj_url, xq_place)
        select_sql = "select `xq_id` from `xq_copy` where `xq_id`='%s'" % xq_id

        try:
            response = cursor.execute(select_sql)
            conn.commit()
            if response == 1:
                print(u'该小区已存在...')
            else:
                try:
                    cursor.execute(insert_sql)
                    conn.commit()
                    print(u'插入成功...')
                except Exception as e:
                    print(u'插入错误...', e)
                    conn.rollback()
        except Exception as e:
            print(u'查询错误...', e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def get_cj_urls(self):
        conn_sel = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianjia')
        cursor = conn_sel.cursor()
        select_sql = "select `xq_cj_url` from xq"
        try:
            cursor.execute(select_sql)
            row = cursor.fetchall()
            for r in row:
                # print(r[0])
                self.cj_list.append(r[0])
            conn_sel.commit()
        except Exception as e:
            print('error1', e)
            conn_sel.rollback()
        finally:
            cursor.close()
            conn_sel.close()


if __name__ == '__main__':
    lianjia = LianJia()
    lianjia.get_xiaoqu_url()

