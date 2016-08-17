from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import scrapy

class SPage(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    
    
    
class TestSpider4(CrawlSpider):
    name = "spiderSO"
    allowed_domains = ["cumulodata.com"]
    start_urls = ["http://www.cumulodata.com/"]

    extractor = SgmlLinkExtractor()

    rules = (
        Rule(extractor,callback='parse_links',follow=True),
        )

    def parse_start_url(self, response):
        list(self.parse_links(response))

    def parse_links(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//a')
        for link in links:
            title = ''.join(link.select('./@title').extract())
            url = ''.join(link.select('./@href').extract())
            meta={'title':title,}
            cleaned_url = "%s/?1" % url if not '/' in url.partition('//')[2] else "%s?1" % url
            yield Request(cleaned_url, callback = self.parse_page, meta=meta,)

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        item=SPage()
        item['url'] = response.url
        item['title']=response.meta['title']
        item['h1']=hxs.select('//h1/text()').extract()
        print(item['url'])
        print(item['title'])
        print(item['h1'])
        return item