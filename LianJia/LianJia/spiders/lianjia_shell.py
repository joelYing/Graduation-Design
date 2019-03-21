#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:joel
# time:2019/3/14 13:05

import math
import pymysql
import requests
import re
from lxml import etree


class LianJia():
    def __init__(self):
        self.cj_list = []
        # 11633 个小区 388页
        self.xiaoqu_list = "https://bj.lianjia.com/xiaoqu/pg{}/"   # 2993
        self.xiaoqu_list_cro11 = "https://bj.lianjia.com/xiaoqu/pg{}cro11/"
        self.xiaoqu_list_cro21 = "https://bj.lianjia.com/xiaoqu/pg{}cro21/"
        # 遍历以上三个链接，100页之后都一样
        self.xiaoqu_cj_list = "https://bj.lianjia.com/chengjiao/pg{}c{}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.feature_en_title = {'小区介绍': 'community_introduce', '户型介绍': 'model_introduce', '税费解析': 'tax_parsing',
                                 '核心卖点': 'sell_point', '售房详情': 'sell_introduce', '装修描述': 'decorate_describe',
                                 '权属抵押': 'power_mortgage', '周边配套': 'surround_facility', '交通出行': 'transportation'
                                 , '适宜人群': 'appropriate_crowd'}

    def get_xiaoqu_url(self):
        s = requests.session()
        for xq_page in range(1, 389):
            print(xq_page)
            r1 = s.get(self.xiaoqu_list_cro21.format(xq_page), headers=self.headers)
            # print(r1.text)
            xq_html = ''
            xq_url_list = re.findall(r'<li class="clear xiaoquListItem".*?<a class="img" href="(.*?)".*?>'
                                     r'.*?<img class="lj-lazy".*?alt="(.*?)">.*?<a title=".*?网签"  href='
                                     r'"(.*?)".*?>.*?</li>', r1.text, re.S)
            for xq in xq_url_list:
                xq_url = xq[0]
                xq_id = re.sub('https://bj\.lianjia\.com/xiaoqu/|/', '', xq_url)
                xq_name = xq[1]
                xq_cj_url = xq[2]
                print(xq_id, xq_url, xq_name, xq_cj_url)
                self.insert(xq_id, xq_url, xq_html, xq_name, xq_cj_url)
            # break

    def w_cj(self):
        with open("D:\\pyprogram\\LianJia\\cj_urls.txt", 'w') as fw:
            for cjurl in self.cj_list:
                fw.writelines(cjurl + '\n')

    def get_cj_info(self):
        s = requests.session()
        for cjurl_num in range(1, len(self.cj_list) + 1):
            cj_id = str(self.cj_list[cjurl_num - 1]).replace('https://bj.lianjia.com/chengjiao/c', '')
            print(str(cjurl_num) + '--' + "成交小区： " + self.cj_list[cjurl_num - 1])
            if cjurl_num > 0:
                r_cjurl = s.get(self.cj_list[cjurl_num - 1], headers=self.headers)
                cjhtml = r_cjurl.text
                if '共找到<span> 0 </span>套北京成交房源' in cjhtml:
                    print("0套成交房源")
                else:
                    housenums = re.findall(r'共找到<span>(.*?)</span>套北京成交房源', cjhtml, re.S)
                    pages = math.ceil(int(str(housenums[0]).strip())/30)
                    for p in range(1, int(pages) + 1):
                        print("第" + str(p) + "页")
                        res = s.get(self.xiaoqu_cj_list.format(str(p), cj_id), headers=self.headers)
                        house_url_list = re.findall(r'<li><a class="img" href="(.*?)".*?><img '
                                                    r'class="lj-lazy".*?alt="(.*?)">', res.text, re.S)
                        for house_urls in house_url_list:
                            house_deal, house_base = {}, {}
                            house_feature = {'community_introduce': '', 'model_introduce': '', 'tax_parsing': '',
                                             'sell_point': '', 'sell_introduce': '', 'decorate_describe': '',
                                             'power_mortgage': '', 'surround_facility': '', 'transportation': '',
                                             'appropriate_crowd': ''}

                            house_id = re.sub('https://bj\.lianjia\.com/chengjiao/|\.html', '', house_urls[0])
                            house_url = house_urls[0]
                            house_title = house_urls[1]
                            print(house_id, house_url, house_title)
                            r_house = s.get(house_url, headers=self.headers)
                            # print(r_house.text)
                            html = etree.HTML(r_house.text)
                            house_dealdate = str([x.text for x in html.xpath('/html/body/div[4]/div/span')][0]).replace(" 成交", '')
                            house_dealprice = [x.text for x in html.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/i')]
                            house_perprice = [x.text for x in html.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/b')]
                            if len(house_dealprice) == 0:
                                house_dealprice = ''
                            else:
                                house_dealprice = house_dealprice[0]
                            if len(house_perprice) == 0:
                                house_perprice = ''
                            else:
                                house_perprice = house_perprice[0]
                            house_pictures = html.xpath('//*[@id="thumbnail2"]/ul/li/img/@src')
                            house_msg = [x.text for x in html.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/*/label')]
                            if len(house_msg) == 0:
                                house_guapai, house_cj_term, p_changetimes, daikan_times, lookatnums, views = '', '', '', '', '', ''
                            else:
                                house_guapai, house_cj_term, p_changetimes, daikan_times, lookatnums, views = house_msg[0], house_msg[1], house_msg[2], house_msg[3], house_msg[4], house_msg[5]
                            house_deal['house_id'], house_deal['house_url'], house_deal['house_title'] = house_id, house_url, house_title
                            house_deal['house_dealdate'], house_deal['house_dealprice'], house_deal['house_perprice'] = house_dealdate, house_dealprice, house_perprice
                            house_deal['house_picturenums'] = str(len(house_pictures))
                            house_deal['house_guapai'], house_deal['house_cjterm'], house_deal['price_changetimes'] = house_guapai, house_cj_term, p_changetimes
                            house_deal['daikan_times'], house_deal['lookatnums'], house_deal['views'] = daikan_times, lookatnums, views

                            self.insert_deal(house_deal)

                            house_place = html.xpath('/html/body/section[2]/div[2]/div/div/div[1]/a/text()')
                            house_baseinfo_title = html.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li/span/text()')
                            house_baseinfo = html.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li/text()')
                            house_dealinfo_title = html.xpath('//*[@id="introduction"]/div[1]/div[2]/div[2]/ul/li/span/text()')
                            house_dealinfo = html.xpath('//*[@id="introduction"]/div[1]/div[2]/div[2]/ul/li/text()')

                            house_base['house_id'], house_base['house_url'], house_base[
                                'house_title'] = house_id, house_url, house_title
                            house_base['house_place'] = house_place[0] + '/' + house_place[1]
                            for i in range(0, 14):
                                house_base[house_baseinfo_title[i]] = str(house_baseinfo[i]).strip()
                            for i in range(0, 6):
                                house_base[house_dealinfo_title[i]] = str(house_dealinfo[i]).strip()

                            self.insert_base(house_base)

                            house_tags = [x.text for x in html.xpath('//*[@id="house_feature"]/div/div[1]/div[2]/a')]
                            house_tese_title = [x.text for x in html.xpath('//*[@class="baseattribute clear"]/div[1]')]
                            house_tese = [x.text for x in html.xpath('//*[@class="baseattribute clear"]/div[2]')]
                            yezhusell = html.xpath('//*[@id="yezhuSell"]/div[2]/div/div/span/text()')
                            if len(yezhusell) == 0:
                                yezhusell = ''
                            else:
                                yezhusell = yezhusell[0]

                            house_feature['house_tags'] = '/'.join(house_tags)
                            house_feature['houseowner_cover'] = yezhusell.replace('\n', '').strip()
                            house_feature['house_id'] = house_id

                            for i in range(0, len(house_tese_title)):
                                if str(house_tese_title[i]) in self.feature_en_title.keys():
                                    house_tese_title_en = self.feature_en_title[str(house_tese_title[i])]
                                    house_feature[house_tese_title_en] = str(house_tese[i]).replace('\n', '').strip()

                            self.insert_feature(house_feature)

                        # print(house_feature)
                # break

    def dict_sql(self, dicts, db):
        names = ','.join(dicts.keys())
        values = ','.join(dicts.values())
        sql = 'insert into ' + db + "(" + names + ") values(" + values + ")"
        return sql

    def insert(self, xq_id, xq_url, xq_html, xq_name, xq_cj_url):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianjia')
        cursor = conn.cursor()

        insert_sql = "insert into `xq` (`xq_id`, `xq_url`, `xq_html`, `xq_name`, `xq_cj_url`)values" \
                     "('%s','%s','%s','%s','%s')" % (xq_id, xq_url, xq_html, xq_name, xq_cj_url)
        select_sql = "select `xq_id` from `xq` where `xq_id`='%s'" % xq_id

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

    def insert_deal(self, house_deal):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianjia')
        cursor = conn.cursor()

        insert_sql = "insert into `house_deal` (`house_id`, `house_url`, `house_title`, `house_dealdate`, " \
                     "`house_dealprice`, `house_perprice`, `house_picturenums`, `house_guapai`, `house_cjterm`, " \
                     "`price_changetimes`, `daikan_times`, `lookatnums`, `views`) values " \
                     "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (house_deal['house_id'],
            house_deal['house_url'], house_deal['house_title'], house_deal['house_dealdate'],
           house_deal['house_dealprice'], house_deal['house_perprice'], house_deal['house_picturenums'],
           house_deal['house_guapai'], house_deal['house_cjterm'], house_deal['price_changetimes'],
           house_deal['daikan_times'], house_deal['lookatnums'], house_deal['views'])
        select_sql = "select `house_id` from `house_deal` where `house_id`='%s'" % house_deal['house_id']

        try:
            response = cursor.execute(select_sql)
            conn.commit()
            if response == 1:
                print(u'该房源deal已存在...')
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

    def insert_base(self, house_base):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianjia')
        cursor = conn.cursor()

        insert_sql = "insert into `house_base` (`house_id`, `house_url`, `house_title`, `house_place`, `house_huxin`, " \
                     "`house_floor`, `build_area`, `house_struc`, `taonei_area`, `house_type`, `building_head`, " \
                     "`build_time`, `house_decorate`,  `build_struc`, `warm_provide`, `elevator`, `right_year`, " \
                     "`have_elevator`, `lianjia_id`, `deal_right`, `guapai_time`, `house_useway`, `house_rightyear`, " \
                     "`house_right`)values" \
                     "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                     "'%s','%s','%s','%s','%s','%s')" % (house_base['house_id'], house_base['house_url'],
                                                         house_base['house_title'], house_base['house_place'],
                                                         house_base['房屋户型'], house_base['所在楼层'],
                                                         house_base['建筑面积'], house_base['户型结构'],
                                                         house_base['套内面积'], house_base['建筑类型'],
                                                         house_base['房屋朝向'], house_base['建成年代'],
                                                         house_base['装修情况'], house_base['建筑结构'],
                                                         house_base['供暖方式'], house_base['梯户比例'],
                                                         house_base['产权年限'], house_base['配备电梯'],
                                                         house_base['链家编号'], house_base['交易权属'],
                                                         house_base['挂牌时间'], house_base['房屋用途'],
                                                         house_base['房屋年限'], house_base['房权所属'])
        select_sql = "select `house_id` from `house_base` where `house_id`='%s'" % house_base['house_id']

        try:
            response = cursor.execute(select_sql)
            conn.commit()
            if response == 1:
                print(u'该房源base已存在...')
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

    def insert_feature(self, house_feature):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='lianjia')
        cursor = conn.cursor()

        insert_sql = "insert into `house_feature` (`house_id`, `house_tags`, `community_introduce`, `model_introduce`" \
                     ", `tax_parsing`, `sell_point`, `houseowner_cover`, `sell_introduce`, `decorate_describe`, " \
                     "`power_mortgage`, `surround_facility`, `transportation`, `appropriate_crowd`)values" \
                     "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (house_feature['house_id'],
                    house_feature['house_tags'], house_feature['community_introduce'], house_feature['model_introduce'],
                    house_feature['tax_parsing'], house_feature['sell_point'], house_feature['houseowner_cover'],
                    house_feature['sell_introduce'], house_feature['decorate_describe'],
                    house_feature['power_mortgage'], house_feature['surround_facility'], house_feature['transportation'],
                    house_feature['appropriate_crowd'])
        select_sql = "select `house_id` from `house_feature` where `house_id`='%s'" % house_feature['house_id']

        try:
            response = cursor.execute(select_sql)
            conn.commit()
            if response == 1:
                print(u'该房源feature已存在...')
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


if __name__ == '__main__':
    lianjia = LianJia()
    # lianjia.get_xiaoqu_url()
    lianjia.get_cj_urls()
    lianjia.get_cj_info()

