import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import AltabankarsItem
from itemloaders.processors import TakeFirst


class AltabankarsSpider(scrapy.Spider):
	name = 'altabankars'
	start_urls = ['https://altabanka.rs/vesti/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="animted-content-inner"]/a[@rel="nofollow"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="elementor-heading-title elementor-size-default"]/text()|//*[contains(concat( " ", @class, " " ), concat( " ", "vestNaslov", " " ))]//text()[normalize-space()]').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "vestSadrzaj", " " ))]//p//text()[normalize-space()]|//*[(@id = "mainSingleVest")]//p//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//*[(@id = "mainSingleVest")]//span/text()|//*[contains(concat( " ", @class, " " ), concat( " ", "vestDatum", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "elementor-clearfix", " " ))]/text()').get()

		item = ItemLoader(item=AltabankarsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
