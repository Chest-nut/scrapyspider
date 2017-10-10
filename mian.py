# -*- coding:utf-8 -*-

import sys
from pathlib import Path

from scrapy.cmdline import execute

sys.path.append(Path(__file__).parent)
execute('scrapy crawl jobbole'.split())
# execute('scrapy crawl zhihu_spider'.split())
# execute('scrapy crawl lagou_spider'.split())