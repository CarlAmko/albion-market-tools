import json
import os
from typing import List, Optional, Union

import requests

import cities
from cities import City
from data.cache import cache_entry, get_item_price_data, generate_entry_key

API_BASE_URL = 'https://albion-online-data.com/api/v2/stats/prices/'

data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/items.json')
with open(data_path) as _json:
	ITEM_DATA = json.load(_json)


def get_prices(item_ids: List[str] = None, city: Union[Optional[City], Optional[List[City]]] = None) -> dict:
	# default to using all item data
	if item_ids is None:
		item_ids = list(map(lambda x: x['UniqueName'], ITEM_DATA))

	# default to all cities
	if not city:
		city = cities.City

	# Wrap singleton city in list for consistency.
	if isinstance(city, City):
		city = [city]

	prices = {}
	items_to_fetch = []
	# First check cache for prices.
	for item_id in item_ids:
		for _city in city:
			result = get_item_price_data(item_id, city=_city)
			if result:
				for key, value in result.items():
					prices[key] = value
			else:
				items_to_fetch.append(item_id)

	# Then request cache misses from API.
	batch = []
	max_batch_size = 100
	for i, item_id in enumerate(items_to_fetch):
		batch.append(item_id)

		if len(batch) == max_batch_size or i == len(item_ids) - 1:
			response = _fetch_current_prices_from_api(batch, city)
			batch.clear()

			# Update cache with data
			for item in response:
				_item_id, _quality, _city = item['item_id'], item['quality'], item['city']
				_prices = {
					'sell_price_min': item['sell_price_min'],
					'sell_price_max': item['sell_price_max'],
					'buy_price_min': item['buy_price_min'],
					'buy_price_max': item['buy_price_max'],
				}
				cache_entry(_item_id, _quality, _city, _prices)
				key = generate_entry_key(_item_id, _quality, _city)
				prices[key] = item

	return prices


# Utility Functions #

def _fetch_current_prices_from_api(item_ids: list, city: Optional[List[City]] = None):
	search_url = API_BASE_URL + ','.join(item_ids)
	params = {}
	if city:
		params['locations'] = ','.join([city.value for city in city])
	return requests.get(search_url, params=params).json()


def find_item_id_by_name(name: str) -> str:
	for item in ITEM_DATA:
		localized_names = item['LocalizedNames']
		if localized_names and localized_names['EN-US'] == name:
			return item['UniqueName']


def generate_item_ids_for_all_enchants(item_id: str = None, name: str = None) -> List[str]:
	if name:
		item_id = find_item_id_by_name(name)
	if item_id:
		return [item_id, f'{item_id}@1', f'{item_id}@2', f'{item_id}@3']
	else:
		raise ValueError(f'No item ids found for name {name} or id {item_id}!')
