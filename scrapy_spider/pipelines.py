# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json

from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors


class ScrapySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JobboleImagesPipeline(ImagesPipeline):
    """添加了获取图片路径功能的ImagesPipeline"""

    def item_completed(self, results, item, info):
        for ok, value in results:
            image_path = value.get('path')
            item['front_img_path'] = image_path
        return item

class JsonPipeline(object):
    """自定义的json文件导出方法"""

    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    # spider结束时会自动调用该函数
    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipeline(object):
    """scrapy提供的json文件导出方法"""

    def __init__(self):
        self.file = open('articleExporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8',
                                         ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MySQLPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
                                    host='127.0.0.1',
                                    user='root',
                                    password='123456',
                                    port=3306,
                                    db='se',
                                    use_unicode=True,
                                    charset='utf8'
                                    )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO jobbole_article(title, create_date, url, url_id)
            VALUES(%s,%s,%s,%s)
        """
        self.cursor.execute(
                            insert_sql, (item['title'], item['create_date'],
                                         item['url'], item['url_id'])
                            )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()

class MySQLTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
                        host = settings['MYSQL_HOST'],
                        user = settings['MYSQL_USER'],
                        password = settings['MYSQL_PASSWORD'],
                        db = settings['MYSQL_DB'],
                        charset = 'utf8',
                        use_unicode = True,
                        cursorclass = MySQLdb.cursors.DictCursor
                        )

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
            INSERT INTO jobbole_article(title, create_date, url, url_id)
            VALUES(%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (item['title'], item['create_date'],
                                    item['url'], item['url_id'])
                        )



if __name__ == '__main__':
    s = '\u7ed9'
    print(type(s))