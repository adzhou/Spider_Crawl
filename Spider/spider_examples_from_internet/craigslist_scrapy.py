import scrapy                               
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor  
from scrapy.selector import HtmlXPathSelector               
from scrapy.item import Item, Field


class CraigslistSampleItem(Item):
	title = Field()
	link = Field()
	                                            
class MySpider(CrawlSpider):                  
    name = "craigs"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/"]

    rules = (
       Rule(LinkExtractor(allow=("index\d+\.html")), callback="parse_items_2", follow=True),

       Rule(LinkExtractor(allow=('\/npo')), callback="parse_items_1"),
       )

    def __init__(self, *a, **kw):
        super(MySpider, self).__init__(*a, **kw)

    def parse_items_1(self, response):
        print(response.url)
        items = []
        hxs = HtmlXPathSelector(response)
        item = CraigslistSampleItem()

        titles = hxs.select("//div")

        for title in titles:
            item["title"] = title.select("//li/a/t ext()").extract()
            item["link"] = title.select("//li/a/@href").extract()
            print(item["title"])
            print(item["link"])                 
            items.append(item)

        return items


    def parse_items_2(self, response):
        print(response.url)
        items = []
        hxs = HtmlXPathSelector(response)
        item = CraigslistSampleItem()

        titles = hxs.select("//p")

        for title in titles:
            item["title"] = title.select("a/text()").extract()
            item["link"] = title.select("a/@href").extract()
            print(item["title"])
            items.append(item)

        return items