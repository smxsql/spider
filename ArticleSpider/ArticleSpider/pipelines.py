# -*- coding: utf-8 -*-
# codecs可以幫助我們避免很多編碼上的繁雜工作
import codecs
import json
import MySQLdb
import MySQLdb.cursors
# 這個adbapi可以把我們mysql中的操作給異步話
from twisted.enterprise import adbapi
from scrapy.exporters import JsonItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodeingPipline(object):
    # 自定義json處理類
    def __init__(self):
        # 打開一個json文件
        self.file = codecs.open('article.json','w',encoding="utf-8")

    # 處理item函數
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_close(self,spider):
        self.file.close()


class MsqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','root','120660','article_spider',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,fav_nums,comment_num,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["front_image_path"],item["praise_nums"],item["fav_nums"],item["comment_num"],item["content"]))

        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    # 類方法會被我們的spider調用的,settings可以把我們載setting文件中的配置給讀出來
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
        host = settings["MYSQL_HOST"],
        db = settings["MYSQL_DBNAME"],
        user = settings["MYSQL_USER"],
        passwd = settings["MYSQL_PASSWORD"],
        charset="utf8",
        cursorclass = MySQLdb.cursors.DictCursor,
        use_unicode = True,
        )
        # 這是一個鏈接池
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted將mysql插入變成異步執行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error) #處理異常

    def handle_error(self,failure):
        #處理異步插入的異常
        print(failure)

    def do_insert(self,cursor,item):

        insert_sql = """
                    insert into article(title,url,create_date,fav_nums,praise_nums,url_object_id)
                    VALUES (%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql,(item["title"],item["url"],item["create_date"],item["fav_nums"],item["praise_nums"],item["url_object_id"]))


# scar在帶的json處理工具
class JsonExporterPipleline(object):
    def __init__(self):
        # b就是以二進制的方式打開
        self.file = open('articleexport.json','wb')
        self.exorter = JsonItemExporter(self.file,encoding = "utf-8",ensure_ascii=False)
        self.exorter.start_exporting()

    def close_spider(self,spider):
            self.exorter.finish_exporting()
            self.file.close()

    def process_item(self, item, spider):
        self.exorter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 調用piepeilens下面的image中的函數
    # 路徑是存儲在result中的

    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok,value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item
