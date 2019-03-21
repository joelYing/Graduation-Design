#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:joel
# time:2018/11/13 17:46

import pymysql

# cj_list = ['https://bj.lianjia.com/chengjiao/c1111027378102/']
cj_list = []


def get_cj_urls():
    """从数据库中获取"""
    conn_sel = pymysql.connect(host='localhost', port=, user='', passwd='', db='lianjia')
    cursor = conn_sel.cursor()
    select_sql = "select `xq_cj_url` from xq"
    try:
        cursor.execute(select_sql)
        row = cursor.fetchall()
        for r in row:
            # print(r[0])
            cj_list.append(r[0])
        conn_sel.commit()
    except Exception as e:
        print('error1', e)
        conn_sel.rollback()
    finally:
        cursor.close()
        conn_sel.close()
