# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver

from scrapy_spider.items import JobboleItem, JobboleItemLoader
from scrapy_spider.utils import common

class JobboleSpider(scrapy.Spider):

    def __init__(self):
        super(JobboleSpider, self).__init__()
        self.browser = webdriver.Chrome(
                executable_path=r'D:\tools\chromedriver_win32\chromedriver.exe')
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self):
        print('爬虫执行结束')
        self.browser.quit()

    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/page/552/']

    def parse(self, response):

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for node in post_nodes:
            image_url = node.css("img::attr(src)").extract_first()

            url = node.css("::attr(href)").extract_first()
            yield Request(url=urljoin(response.url, url),
                          meta={'front_img_url': urljoin(response.url, image_url)},
                          callback=self.parse_detial
                          )

        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)


    def parse_detial(self, response):
        """提取文章的具体内容"""

        # front_img_url = response.meta.get('front_img_url')  # 文章封面图地址
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        # create_date = response.xpath("//div[@class='entry-meta']\
        #                 /p/text()").extract_first().strip().replace(' ·', '')
        # try:
        #     create_date = datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception:
        #     create_date = datetime.now().date()
        # like_nums = response.xpath("//span[contains(@class, 'vote-post-up')]\
        #                             /h10/text()").extract_first()
        # if like_nums is None:
        #     like_nums = 0
        # else:
        #     like_nums = int(like_nums)
        # bookmark_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]\
        #                     /text()").extract_first().replace('收藏', '').strip()
        # if bookmark_nums is '': # 和 is None 有所区别
        #     bookmark_nums = 0
        # else:
        #     bookmark_nums = int(bookmark_nums)
        # comment_nums = response.xpath("//span[contains(@class, 'hide-on-480')]\
        #                     /text()").extract_first().replace('评论', '').strip()
        # if comment_nums is '':
        #     comment_nums = 0
        # else:
        #     comment_nums = int(comment_nums)
        # content = response.xpath("//div[@class='entry']").extract_first()
        # tag_list = response.xpath("//div[@class='entry-meta']//a/text()").extract()
        # tag_list = [each for each in tag_list if not each.strip().endswith('评论')]
        # tags = ','.join(tag_list)
        #
        # item = JobboleItem()
        # item['title'] = title
        # item['create_date'] = create_date
        # item['tags'] = tags
        # item['url'] = response.url
        # item['url_id'] = common.get_md5(response.url)
        # item['front_img_url'] = [front_img_url]
        # item['like_nums'] = like_nums
        # item['bookmark_nums'] = bookmark_nums
        # item['comment_nums'] = comment_nums
        # item['content'] = content

        # 使用ItemLoader填充item
        item_loader = JobboleItemLoader(item=JobboleItem(), response=response)
        item_loader.add_xpath('title', "//div[@class='entry-header']/h1/text()")
        item_loader.add_xpath('create_date', "//div[@class='entry-meta']/p/text()")
        item_loader.add_xpath('tags', "//div[@class='entry-meta']//a/text()")
        item_loader.add_xpath('like_nums',"//span[contains(@class,\
                                'vote-post-up')]/h10/text()")
        item_loader.add_xpath('bookmark_nums',"//span[contains(@class,\
                                'bookmark-btn')]/text()")
        item_loader.add_xpath('comment_nums',"//span[contains(@class,\
                                'hide-on-480')]/text()")
        item_loader.add_xpath('content', "//div[@class='entry']")
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_id', common.get_md5(response.url))
        front_img_url = response.meta.get('front_img_url')  # 文章封面图地址
        item_loader.add_value('front_img_url', [front_img_url])

        item = item_loader.load_item()
        yield item