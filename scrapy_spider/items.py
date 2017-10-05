# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobboleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field()
    like_nums = scrapy.Field()
    bookmark_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
