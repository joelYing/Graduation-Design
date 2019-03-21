# -*- coding: utf-8 -*-
import math
import re
import scrapy
from lxml import etree
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from LianJia.items import HouseDealItem, HouseBaseItem, HouseFeatureItem
from LianJia.spiders.xqseletor import cj_list, get_cj_urls


class WiwjSpider(scrapy.Spider):
    """
    不能在settings添加 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None, 以及需要 ROBOTSTXT_OBEY = True
    dont_filter = true 误入爬行循环！
    """
    name = 'lianjia'
    allowed_domains = ['lianjia.com']

    # 11633 个小区 388页
    xiaoqu_list = "https://bj.lianjia.com/xiaoqu/pg{}/"  # 2993
    xiaoqu_list_cro11 = "https://bj.lianjia.com/xiaoqu/pg{}cro11/"
    xiaoqu_list_cro21 = "https://bj.lianjia.com/xiaoqu/pg{}cro21/"
    # 遍历以上三个链接，100页之后都一样
    xiaoqu_cj_list = "https://bj.lianjia.com/chengjiao/pg{}c{}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.102 Safari/537.36'
    }
    feature_en_title = {
        '小区介绍': 'community_introduce', '户型介绍': 'model_introduce',
        '税费解析': 'tax_parsing', '核心卖点': 'sell_point',
        '售房详情': 'sell_introduce', '装修描述': 'decorate_describe',
        '权属抵押': 'power_mortgage', '周边配套': 'surround_facility',
        '交通出行': 'transportation', '适宜人群': 'appropriate_crowd'
    }
    base_en_title = {
        '房屋户型': 'house_huxin', '所在楼层': 'house_floor',
        '建筑面积': 'build_area', '户型结构': 'house_struc',
        '套内面积': 'taonei_area', '建筑类型': 'house_type',
        '房屋朝向': 'building_head', '建成年代': 'build_time',
        '装修情况': 'house_decorate', '建筑结构': 'build_struc',
        '供暖方式': 'warm_provide', '梯户比例': 'elevator',
        '产权年限': 'right_year', '配备电梯': 'have_elevator',
        '链家编号': 'lianjia_id', '交易权属': 'deal_right',
        '挂牌时间': 'guapai_time', '房屋用途': 'house_useway',
        '房屋年限': 'house_rightyear', '房权所属': 'house_right',
    }
    get_cj_urls()

    def start_requests(self):
        for cjurl_num in range(1, len(cj_list) + 1):
            cj_id = str(cj_list[cjurl_num - 1]).replace('https://bj.lianjia.com/chengjiao/c', '')
            print(str(cjurl_num) + '--' + "成交小区： " + cj_list[cjurl_num - 1])
            if cjurl_num > 0:
                yield Request(cj_list[cjurl_num - 1], callback=self.parse,
                              meta={'cj_id': cj_id}, dont_filter=False)

    def parse(self, response):
        cj_id = response.meta['cj_id']
        if '共找到<span> 0 </span>套北京成交房源' in response.text:
            print("0套成交房源")
        else:
            housenums = re.findall(r'共找到<span>(.*?)</span>套北京成交房源', response.text, re.S)
            pages = math.ceil(int(str(housenums[0]).strip()) / 30)
            for p in range(1, int(pages) + 1):
                print("第" + str(p) + "页")
                yield Request(self.xiaoqu_cj_list.format(str(p), cj_id), callback=self.parse_house_info,
                              dont_filter=False)

    def parse_house_info(self, response):
        house_url_list = re.findall(r'<li><a class="img" href="(.*?)".*?><img '
                                    r'class="lj-lazy".*?alt="(.*?)">', response.text, re.S)
        for house_urls in house_url_list:
            house_id = re.sub('https://bj\.lianjia\.com/chengjiao/|\.html', '', house_urls[0])
            house_url = house_urls[0]
            house_title = house_urls[1]
            print(house_id, house_url, house_title)
            yield Request(house_url, callback=self.parse_house_detail,
                          meta={'house_url': house_url, 'house_id': house_id, 'house_title': house_title},
                          dont_filter=False)

    def parse_house_detail(self, response):
        house_deal, house_base = HouseDealItem(), HouseBaseItem()
        house_feature = HouseFeatureItem()
        # 补齐房屋特色的字段
        house_feature_title = {'community_introduce': '', 'model_introduce': '', 'tax_parsing': '',
                               'sell_point': '', 'sell_introduce': '', 'decorate_describe': '',
                               'power_mortgage': '', 'surround_facility': '', 'transportation': '',
                               'appropriate_crowd': ''}
        for title in house_feature_title.keys():
            house_feature[title] = ''

        house_id, house_url, house_title = \
            response.meta['house_id'], response.meta['house_url'], response.meta['house_title']

        html = etree.HTML(response.text)
        house_dealdate = str([x.text for x in html.xpath('/html/body/div[4]/div/span')][0]).replace(
            " 成交", '')
        house_dealprice = [x.text for x in
                           html.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/i')]
        house_perprice = [x.text for x in
                          html.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/b')]
        if len(house_dealprice) == 0:
            house_dealprice = ''
        else:
            house_dealprice = house_dealprice[0]
        if len(house_perprice) == 0:
            house_perprice = ''
        else:
            house_perprice = house_perprice[0]
        house_pictures = html.xpath('//*[@id="thumbnail2"]/ul/li/img/@src')
        house_msg = [x.text for x in
                     html.xpath('/html/body/section[1]/div[2]/div[2]/div[3]/*/label')]
        if len(house_msg) == 0:
            house_guapai, house_cj_term, p_changetimes, daikan_times, lookatnums, views = '', '', '', '', '', ''
        else:
            house_guapai, house_cj_term, p_changetimes, daikan_times, lookatnums, views = \
                house_msg[0], house_msg[1], house_msg[2], house_msg[3], house_msg[4], house_msg[5]
        house_deal['house_id'], house_deal['house_url'], house_deal[
            'house_title'] = house_id, house_url, house_title
        house_deal['house_dealdate'], house_deal['house_dealprice'], house_deal[
            'house_perprice'] = house_dealdate, house_dealprice, house_perprice
        house_deal['house_picturenums'] = str(len(house_pictures))
        house_deal['house_guapai'], house_deal['house_cjterm'], house_deal[
            'price_changetimes'] = house_guapai, house_cj_term, p_changetimes
        house_deal['daikan_times'], house_deal['lookatnums'], house_deal[
            'views'] = daikan_times, lookatnums, views

        # self.insert_deal(house_deal)
        yield house_deal

        house_place = html.xpath('/html/body/section[2]/div[2]/div/div/div[1]/a/text()')
        house_baseinfo_title = html.xpath(
            '//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li/span/text()')
        house_baseinfo = html.xpath('//*[@id="introduction"]/div[1]/div[1]/div[2]/ul/li/text()')
        house_dealinfo_title = html.xpath(
            '//*[@id="introduction"]/div[1]/div[2]/div[2]/ul/li/span/text()')
        house_dealinfo = html.xpath('//*[@id="introduction"]/div[1]/div[2]/div[2]/ul/li/text()')

        house_base['house_id'], house_base['house_url'], house_base[
            'house_title'] = house_id, house_url, house_title
        house_base['house_place'] = house_place[0] + '/' + house_place[1]
        for i in range(0, 14):
            house_base[self.base_en_title[house_baseinfo_title[i]]] = str(house_baseinfo[i]).strip()
        for i in range(0, 6):
            house_base[self.base_en_title[house_dealinfo_title[i]]] = str(house_dealinfo[i]).strip()

        # self.insert_base(house_base)
        yield house_base

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

        # self.insert_feature(house_feature)
        yield house_feature
        # print(house_deal, '\n', house_base, '\n', house_feature)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl("lianjia")
    process.start()
