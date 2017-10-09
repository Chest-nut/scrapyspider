# -*- coding: utf-8 -*-

import json
import re

import scrapy


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    custom_settings = {'COOKIES_ENABLED': True}

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/', headers=self.headers,
                               callback=self.login)]

    def login(self, response):
        result = re.search('.*name="_xsrf" value="(.*?)"', response.text)
        if result:
            xsrf = result.group(1)
            post_url = 'https://www.zhihu.com/login/phone_num'
            post_data = {
                    '_xsrf': xsrf,
                    'account': '',
                    'password': ''
                    }
            return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.is_login
            )]

    def is_login(self, response):
        text = response.text
