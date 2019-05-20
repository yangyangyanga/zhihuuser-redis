# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ZhihuuserPipeline(object):
    collection_name = 'users'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # # 连接服务器
        # conn = MongoClient("localhost", 27017)
        # # 连接数据库
        # db = conn.mydb
        # # 获取集合
        # collection = db.student
        # print("集合查询： ", collection.find())
        # for row in collection.find():
        #     print("row == ", row)
        #     print(type(row))
        # conn.close()
        self.db[self.collection_name].update({'url_token': item['url_token']}, {'$set': dict(item)}, True, True)
        print("数据插入")
        return item
