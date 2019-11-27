# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Src.MySQLHelper.MySqlHelper import MySqlHelper

class MySQLPipline(object):
    def open_spider(self, spider):
        print("start crawling")
        self.helper = MySqlHelper()
        self.helper.connect()

    def close_spider(self, spider):
        print("finish crawling")
        self.helper.close()

    def submit(self, item):
        sql = "INSERT INTO news(title, content, type, url, time) VALUES(%s, %s, %s, %s, %s)"
        self.helper.insert(sql, item["title"], item["content"], item["type"], item['url'], item["time"])

    def process_item(self, item, spider):
        if(item != None):
            self.submit(item)
        return
