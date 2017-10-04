# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112569/']

    def parse(self, response):
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        create_time = response.xpath("//div[@class='entry-meta']\
                        /p/text()").extract()[0].strip().replace(' ·', '')
        like_nums = response.xpath("//span[contains(@class, 'vote-post-up')]\
                                    /h10/text()").extract()[0]
        bookmark_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]\
                            /text()").extract()[0].replace('收藏', '').strip()
        comment_nums = response.xpath("//span[contains(@class, 'hide-on-480')]\
                            /text()").extract()[0].replace('评论', '').strip()
        contents = response.xpath("//div[@class='entry']").extract()[0]
        tag_list = response.xpath("//div[@class='entry-meta']//a/text()").extract()
        tag_list = [each for each in tag_list if not each.strip().endswith('评论')]
        tags = ','.join(tag_list)
        pass
