import scrapy
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from twisted.internet import reactor

import re
import ast

tables = []

class MySpider(CrawlSpider):
	name = 'cname'
	allowed_domains = ['digikey.com']

	def __init__(self, *args, **kwargs):
		super(MySpider, self).__init__(*args, **kwargs)
		print kwargs.get('url')
		self.start_urls = [kwargs.get('url')]

	def parse(self, response):
		print '==========----------------==============='
		hxs = HtmlXPathSelector(response)

class IndexSpider(CrawlSpider):
	name = 'index'
	allowed_domains = ['digikey.com']
	start_urls = ['http://www.digikey.com/product-search/en']

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		for item in hxs.select("//ul[@class='catfiltersub']/li"):
			rec = {}
			rec['name'] = item.xpath("a[@class='catfilterlink']/text()").extract()[0]
			pages = int(re.search(r'\d+', item.xpath("text()").extract()[0]).group())
			rec['start_urls'] = [	"http://www.digikey.com/product-search/en" + 
							item.xpath("a[@class='catfilterlink']/@href").extract()[0] + 
							"/page/%s" % page for page in xrange(1, int(pages / 25) + 2 )
						]
			tables.append(rec)
			break

process = CrawlerProcess({
	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(IndexSpider)
process.start() 
process.stop()

spider_lst = []

sub_process = CrawlerProcess({
		'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	 })

for item in  tables:
	print item['name']
	sub_process.crawl(MySpider(url=item['start_urls']))
	sub_process.start()
	break
print '==== END ======='