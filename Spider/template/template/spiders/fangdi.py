# -*- coding: utf-8 -*-
import scrapy


class FangdiSpider(scrapy.Spider):
    name = "fangdi"
    allowed_domains = ["fangdi.com"]
    start_urls = (
        'http://www.fangdi.com/',
    )

    def parse(self, response):
        pass
