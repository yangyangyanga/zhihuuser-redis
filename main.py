# -*- coding:utf-8 -*-
"""
# @PROJECT: zhihuuser
# @Author: admin
# @Date:   2019-05-16 14:35:49
# @Last Modified by:   admin
# @Last Modified time: 2019-05-16 14:35:49
"""
from scrapy import cmdline

cmdline.execute("scrapy crawl zhihu".split())