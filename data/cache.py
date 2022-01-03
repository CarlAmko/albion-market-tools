import json
import os
from typing import Union

import redis

from cities import City

config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')
with open(config_path) as _config:
	config = json.load(_config)

# Open connection to Redis for caching
cache = redis.Redis(host=config['redis_url'], port=config['redis_port'], decode_responses=True)


def generate_entry_key(item_id: str, quality: int, city: Union[str, City]) -> str:
	if isinstance(city, City):
		return f'{item_id}:{quality}:{city.value}'
	else:
		return f'{item_id}:{quality}:{city}'


def check_cache(item_id: str, quality: int, city: City) -> bool:
	key = generate_entry_key(item_id, quality, city)
	return cache.exists(key) != 0


def cache_item_prices(item_id: str, quality: int, city: City, values: dict):
	key = generate_entry_key(item_id, quality, city)
	cache.hmset(key, values)


def get_item_price(item_id: str, quality: int = None, city: City = None) -> dict:
	def create_key_match_pattern():
		return f'{item_id}:{quality if quality else "*"}:{city.value if city else "*"}'

	match_pattern = create_key_match_pattern()
	keys = cache.keys(match_pattern)

	res = {}
	for key in keys:
		res[key] = cache.hgetall(key)
	return res
