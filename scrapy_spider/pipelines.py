# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

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
