# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request

from scrapy_spider.items import JobboleItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for node in post_nodes:
            image_url = node.css("img::attr(src)").extract_first()
            url = node.css("::attr(href)").extract_first()
            yield Request(url=urljoin(response.url, url),
                          meta={'front_img_url': image_url},
                          callback=self.parse_detial
                          )

        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)


    def parse_detial(self, response):
        """提取文章的具体内容"""

        front_img_url = response.meta.get('front_img_url')  # 文章封面图地址
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        create_date = response.xpath("//div[@class='entry-meta']\
                        /p/text()").extract_first().strip().replace(' ·', '')
        like_nums = response.xpath("//span[contains(@class, 'vote-post-up')]\
                                    /h10/text()").extract_first()
        if like_nums is None:
            like_nums = 0
        else:
            like_nums = int(like_nums)
        bookmark_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]\
                            /text()").extract_first().replace('收藏', '').strip()
        if bookmark_nums is None:
            bookmark_nums = 0
        else:
            bookmark_nums = int(bookmark_nums)
        comment_nums = response.xpath("//span[contains(@class, 'hide-on-480')]\
                            /text()").extract_first().replace('评论', '').strip()
        if comment_nums is None:
            comment_nums = 0
        else:
            comment_nums = int(comment_nums)
        content = response.xpath("//div[@class='entry']").extract_first()
        tag_list = response.xpath("//div[@class='entry-meta']//a/text()").extract()
        tag_list = [each for each in tag_list if not each.strip().endswith('评论')]
        tags = ','.join(tag_list)

        item = JobboleItem()
        item['title'] = title
        item['create_date'] = create_date
        item['url'] = response.url
        # item['url_id'] = url_id
        item['front_img_url'] = [front_img_url]
        # item['front_img_path'] = front_img_path
        item['like_nums'] = like_nums
        item['bookmark_nums'] = bookmark_nums
        item['comment_nums'] = comment_nums
        item['tags'] = tags
        item['content'] = content

        yield item
