# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

# CREATE TABLE `house_base` (
#   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `house_id` varchar(64) CHARACTER SET utf8 NOT NULL,
#   `house_url` varchar(255) DEFAULT NULL,
#   `house_title` varchar(255) DEFAULT NULL,
#   `house_place` varchar(127) DEFAULT NULL,
#   `house_huxin` varchar(127) DEFAULT '' COMMENT '房屋户型',
#   `house_floor` varchar(127) DEFAULT '' COMMENT '所在楼层',
#   `build_area` varchar(127) DEFAULT NULL COMMENT '建筑面积',
#   `house_struc` varchar(127) DEFAULT NULL COMMENT '户型结构',
#   `taonei_area` varchar(127) DEFAULT NULL COMMENT '套内面积',
#   `house_type` varchar(127) DEFAULT NULL COMMENT '建筑类型',
#   `building_head` varchar(127) DEFAULT NULL COMMENT '房屋朝向',
#   `build_time` varchar(127) DEFAULT NULL COMMENT '建成年代',
#   `house_decorate` varchar(127) DEFAULT NULL COMMENT '装修情况',
#   `build_struc` varchar(127) DEFAULT NULL COMMENT '建筑结构',
#   `warm_provide` varchar(127) DEFAULT NULL COMMENT '供暖方式',
#   `elevator` varchar(127) DEFAULT NULL COMMENT '梯户比例',
#   `right_year` varchar(127) DEFAULT NULL COMMENT '产权年限',
#   `have_elevator` varchar(127) DEFAULT NULL COMMENT '配备电梯',
#   `lianjia_id` varchar(127) DEFAULT NULL COMMENT '链家编号',
#   `deal_right` varchar(127) DEFAULT NULL COMMENT '交易权属',
#   `guapai_time` varchar(127) DEFAULT NULL COMMENT '挂牌时间',
#   `house_useway` varchar(127) DEFAULT NULL COMMENT '房屋用途',
#   `house_rightyear` varchar(127) DEFAULT NULL COMMENT '房屋年限',
#   `house_right` varchar(127) DEFAULT NULL COMMENT '房权所属',
#   PRIMARY KEY (`id`),
#   KEY `house_id` (`house_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1237 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

# CREATE TABLE `house_deal` (
#   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `house_id` varchar(64) CHARACTER SET utf8 NOT NULL,
#   `house_url` varchar(255) DEFAULT NULL,
#   `house_title` varchar(255) DEFAULT NULL,
#   `house_dealdate` varchar(128) DEFAULT NULL,
#   `house_dealprice` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `house_perprice` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `house_picturenums` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `house_guapai` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `house_cjterm` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `price_changetimes` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `daikan_times` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `lookatnums` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   `views` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   KEY `house_id` (`house_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1268 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

# CREATE TABLE `house_feature` (
#   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `house_id` varchar(127) NOT NULL,
#   `house_tags` varchar(127) DEFAULT NULL COMMENT '房源标签',
#   `community_introduce` text COMMENT '小区介绍',
#   `model_introduce` text COMMENT '户型介绍',
#   `tax_parsing` text COMMENT '税费解析',
#   `sell_point` text COMMENT '核心卖点',
#   `houseowner_cover` text COMMENT '房主自荐',
#   `sell_introduce` text COMMENT '售房详情',
#   `decorate_describe` text COMMENT '装修描述',
#   `power_mortgage` text COMMENT '权属抵押',
#   `surround_facility` text COMMENT '周边配套',
#   `transportation` text COMMENT '交通出行',
#   `appropriate_crowd` text COMMENT '适宜人群',
#   PRIMARY KEY (`id`),
#   KEY `house_id` (`house_id`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=1289 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;





