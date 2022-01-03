from typing import Optional

import data.prefix as prefix
import datafetch
from cities import City
from data.cache import generate_entry_key


def get_items_required_for_enchant(item_id: str):
	base_enchant_quantity = 48
	if prefix.is_shoe(item_id) or prefix.is_head(item_id):
		return base_enchant_quantity
	elif prefix.is_armor(item_id):
		return base_enchant_quantity * 2
	elif prefix.is_1h(item_id):
		return base_enchant_quantity * 3
	elif prefix.is_2h(item_id):
		return base_enchant_quantity * 4


def get_enchant_item_prices(enchant_level: int, tier: int, city: City):
	_prefix = prefix.TIER_PREFIXES[tier]

	def create_enchant_name():
		if enchant_level == 0:
			return f'{_prefix}\'s Rune'
		elif enchant_level == 1:
			return f'{_prefix}\'s Soul'
		else:
			return f'{_prefix}\'s Relic'

	if _prefix:
		enchant_name = create_enchant_name()
		enchant_id = datafetch.find_item_id_by_name(enchant_name)
		key = generate_entry_key(enchant_id, 1, city)
		return datafetch.get_prices([enchant_id], city=city)[key]

	return None


def calculate_enchant_profits(item_id: str, city: City) -> Optional[dict]:
	all_item_ids = datafetch.generate_item_ids_for_all_enchants(item_id=item_id)
	num_enchant_items = get_items_required_for_enchant(item_id)
	if not num_enchant_items:
		return None

	item_price_data = datafetch.get_prices(all_item_ids, city=city)
	profits = {}
	for quality in range(1, 6):
		for i in range(len(all_item_ids) - 1):
			curr_id = all_item_ids[i]
			next_id = all_item_ids[i + 1]
			key = generate_entry_key(curr_id, quality, city)
			next_key = generate_entry_key(next_id, quality, city)

			curr_price = item_price_data[key]['sell_price_min']
			next_price = item_price_data[next_key]['sell_price_min']
			base_profit = int(next_price) - int(curr_price)

			tier = prefix.get_tier(item_id)
			enchant_cost = int(get_enchant_item_prices(enchant_level=i, tier=tier, city=city)['sell_price_min'])
			net_profit = base_profit - (enchant_cost * num_enchant_items)
			# Ignore losses.
			if net_profit > 0:
				profits[key] = net_profit

	return profits

# TODO: This is expensive. There are currently 1886 equipment items that can be enchanted, and API is rate-limited to
# TODO:  300 calls / 5 mins.
# def find_best_enchants(city: City) -> dict:
# 	results = {}
# 	for item in datafetch.ITEM_DATA:
# 		unique_name = item['UniqueName']
# 		# Only look at base enchant item, so we can force a particular order
# 		if '@' not in unique_name and prefix.is_equipment(unique_name):
# 			profits = calculate_enchant_profits(unique_name, city=city)
# 			if profits:
# 				results.update(profits)
# 	return results
