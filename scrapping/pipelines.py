from data.cache import cache
from itemadapter import ItemAdapter

from scrapping.spiders.crafting_reqs_spider import CraftingRequirementsSpider


class CacheItemPipeline:
	def process_item(self, item, spider):
		adapter = ItemAdapter(item)
		if isinstance(spider, CraftingRequirementsSpider):
			cache.set(name=f'focus:{item["item"]}', value=item['base_craft_focus'])
		return item
