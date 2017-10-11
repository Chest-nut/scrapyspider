# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from datetime import datetime
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
import scrapy


class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def date_convert(value):
    try:
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception:
        create_date = datetime.now().date()
    return create_date

def remove_comment_tags(value):
    if '评论' in value:
        return ''
    else:
        return value

def get_nums(value):
    match_re = re.match(r'.*?(\d+).*', value)
    if match_re:
        return int(match_re.group(1))
    else:
        return 0

def no_change(value):
    """用于覆盖default_output_processor"""
    return value

class JobboleItemLoader(ItemLoader):
    """自定义 ItemLoader，重载了 default_output_processor"""
    default_output_processor = TakeFirst()

class JobboleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    url_id = scrapy.Field()
    content = scrapy.Field()
    front_img_url = scrapy.Field(
        output_processor=MapCompose(no_change)
    )
    front_img_path = scrapy.Field()
    like_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    bookmark_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(',')
    )
