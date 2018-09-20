# -*- coding: utf-8 -*-

import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunblogsPipeline(object):

    # 初始化的时候连接本地数据库
    def __init__(self):
        self.conn = pymysql.connect(host = "127.0.0.1", user = "root", password = "root", database = "hexunblog")

    def process_item(self, item, spider):
        # 每一个博文列表页都有多个文章，所以此处需要遍历
        for index in range(0, len(item["articleName"])):
            articleName = item["articleName"][0]
            articleUrl = item["articleUrl"][0]
            articleClicks = item["articleClicks"][0]
            articleComments = item["articleComments"][0]
            sql = "insert into blog(articleName, articleUrl, articleClicks, articleComments) " \
                  "values ('"+articleName+"', '"+articleUrl+"', '"+articleClicks+"', '"+articleComments+"')"
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql)
                self.conn.commit()
            except:
                self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.conn.close()