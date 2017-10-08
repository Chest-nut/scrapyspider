# -*- coding:utf-8 -*-

import random
import re

import requests
from scrapy.selector import Selector

def _crawl_ip():
    IP_list = []
    url = 'http://www.xicidaili.com/nn/'
    useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    headers = {'User-Agent': useragent}
    response = requests.get(url, headers=headers)
    selector = Selector(response)
    trs = selector.css('tr[class]')
    for tr in trs:
        IP = tr.css('td:nth-child(2)').extract_first()
        IP = re.search(r'(\d.*\d)', IP).group(1)
        port = tr.css('td:nth-child(3)').extract_first()
        port = re.search(r'(\d.*\d)', port).group(1)
        IP_list.append('%s:%s' %(IP, port))
    return IP_list

def get_IP():
    IP_list = _crawl_ip()
    IP = random.sample(IP_list, 1)[0]
    return IP
