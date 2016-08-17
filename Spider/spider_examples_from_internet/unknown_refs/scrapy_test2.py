from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.http import Request

class ESpider(CrawlSpider):
    name = "pratt"
    allowed_domains = ["pratt.edu"]
    start_urls = ["https://www.pratt.edu/academics/architecture/ug_dept_architecture/faculty_and_staff/?id=01302"]

    rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('/html/body/div[3]/div/div[2]/div/div/p/a',))
    , callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        contacts = Selector(response)
        print contacts.xpath('/html/body/div[3]/div/div[2]/table/tbody/tr[2]/td[2]/h3').extract()
        print contacts.xpath('/html/body/div[3]/div/div[2]/table/tbody/tr[2]/td[2]/a').extract()