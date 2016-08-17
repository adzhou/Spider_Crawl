import scrapy
from tutorial.items import FangdiItem


class FangdiSpider(scrapy.Spider):
    name = "fangdi"
    allowed_domains = ["fangdi.com.cn"]
    start_urls = [
        "http://www.fangdi.com.cn/MoreDis4Type.asp?TYPE=AllBargain",
        "http://www2.fangdi.com.cn/finalndhouse/info_GP.asp"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = FangdiItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item


