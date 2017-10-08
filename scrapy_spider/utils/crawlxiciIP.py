# -*- coding:utf-8 -*-

import random
import re

import requests
from scrapy.selector import Selector

class GetIP(object):
    def __init__(self):
        self.IP_list = []
        self._crawl_ip()

    def _crawl_ip(self):
        useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36' \
                    '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        headers = {'User-Agent': useragent}
        for i in [1,2]:
            url = 'http://www.xicidaili.com/nn/{0}'.format(i)
            response = requests.get(url, headers=headers)
            selector = Selector(response)
            trs = selector.css('tr[class]')
            for tr in trs:
                IP = tr.css('td:nth-child(2)::text').extract_first()
                port = tr.css('td:nth-child(3)::text').extract_first()
                type = tr.css('td:nth-child(6)::text').extract_first()
                if type == 'HTTP':
                    self.IP_list.append('%s:%s' %(IP, port))

    def _is_usable_ip(self, ip):
        url = 'https://www.baidu.com'
        proxy_dic = {'http': ip}
        try:
            response = requests.get(url, proxies=proxy_dic)
            if 200 <= response.status_code < 300:
                print('IP可用')
                return True
        except Exception as e:
            print(e)
            return False

    def get_IP(self):
        IP = random.sample(self.IP_list, 1)[0]
        if self._is_usable_ip(IP):
            return IP
        else:
            return self.get_IP()
