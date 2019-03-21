#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-5

import re
from random import choice
import requests


class Wiwj(object):
    def __init__(self):
        """
        75163套 按每页30个 共有2506页
        """
        self.start_url = 'https://sh.5i5j.com/ershoufang/'
        # self.proxies = {"http": "http://localhost:1080", "https": "http://localhost:1080", }

    def jpg_tool(self, text):
        house_jpg = ''
        if 'src' in text:
            house_jpg = re.findall(r'src="(.*?)".*?', text, re.S)[0]
        return house_jpg

    def div_tool(self, text):
        text = re.sub('<.*?>| i |<!--|-->', ' ', text)
        return text

    @staticmethod
    def getadsl(res):
        """ 随机取ip """
        proxies = {"http": "http://" + choice(res['data']), }
        # print(proxies)
        return proxies

    def gethouselist(self):
        s = requests.session()
        res = s.get('http://', headers={}).json()
        r = s.get(self.start_url, proxies=self.getadsl(res))
        print(r.text)
        # 二手房url，封面图片（如果有src在内则有图片），标题，第一行，第二行，第三行，总价，单价，标签
        basic_info_list = re.findall(r'<div class="listImg".*?><a href="(.*?)" target="_blank">.*?<img class='
                                     r'"lazy" (.*?)title="(.*?)".*?>.*?<!-- <p>.*?</p> -->.*?<i class="i_01">'
                                     r'</i>(.*?)</p>.*?<i class="i_02"></i>(.*?)</p>.*?<i class="i_03"></i>(.*?)</p>'
                                     r'.*?<p class="redC">(.*?)</p>.*?<p>.*?(\d+).*?</p>.*?<div class="listTag">(.*?)<'
                                     r'/div>', r.text, re.S)
        if basic_info_list:
            for basic_info in basic_info_list:
                # print(basic_info)
                house_url = 'https://sh.5i5j.com' + basic_info[0]
                house_jpg = self.jpg_tool(basic_info[1])
                house_title = basic_info[2]
                first_line = basic_info[3].split(" · ")
                # house_type = first_line[0]
                # house_m2 = first_line[1]
                # house_direction = first_line[2]
                second_line = basic_info[4].split(" · ")
                for i in range(0, len(second_line)):
                    second_line[i] = self.div_tool(second_line[i])
                third_line = basic_info[5].split(" · ")
                house_price = self.div_tool(basic_info[6])
                house_m2_price = basic_info[7]
                house_tag = self.div_tool(basic_info[8])
                # print(second_line)
                print(house_url, house_jpg, house_title, first_line, second_line, third_line, house_price, house_m2_price, house_tag)


if __name__ == '__main__':
    wiwj = Wiwj()
    wiwj.gethouselist()

