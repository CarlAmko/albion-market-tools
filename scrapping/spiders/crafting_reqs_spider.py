import scrapy


class CraftingRequirementsSpider(scrapy.Spider):
	name = "crafting_reqs"

	def start_requests(self):
		item_id = getattr(self, 'item_id', None)
		if not item_id:
			raise ValueError(f'Item id is required to run.')

		url = f'https://www.albiononline2d.com/en/item/id/{item_id}/craftingrequirements'
		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response, **kwargs):
		for result in response.xpath("//td[contains(text(), 'craftingfocus')]/../td[2]"):
			yield {
				'item': getattr(self, 'item_id', None),
				'base_craft_focus': result.css('td::text').get()
			}
