import json

import redis
import requests

import cities

API_BASE_URL = 'http://albion-online-data.com/api/v2/stats/prices/'

# Parse item data
with open('data/items.json') as _json:
    ITEM_DATA = json.load(_json)

# Open connection to Redis for caching
with open('config.json') as _config:
    config = json.load(_config)

r = redis.Redis(host=config['redis_url'], port=config['redis_port'], password=config['redis_password'],
                decode_responses=True)


def generate_cache_key(item_id: str, city: str, quality: int) -> str:
    return f'{item_id}:{city}:{quality}'


def check_cache(item_id: str, city: str, quality: int) -> bool:
    key = generate_cache_key(item_id, city, quality)
    return r.exists(key)


def fetch_prices_and_update_cache(item_ids=None, city=None):
    # default to using all item data
    if item_ids is None:
        item_ids = list(map(lambda x: x['UniqueName'], ITEM_DATA))

    def fetch_current_prices(_item_ids: list, _city: str = None):
        search_url = API_BASE_URL + ','.join(_item_ids)
        params = {}
        if _city:
            params = {'locations': _city}
        return requests.get(search_url, params=params).json()

    batch = []
    for i, item_id in enumerate(item_ids):
        batch.append(item_id)

        if len(batch) == 100 or i == len(item_ids) - 1:
            response = fetch_current_prices(batch, city)
            batch.clear()

            # Update cache with data
            for item in response:
                _item_id, _city, _quality = item['item_id'], item['city'], item['quality']
                _prices = {
                    'sell_price_min': item['sell_price_min'],
                    'sell_price_max': item['sell_price_max'],
                    'buy_price_min': item['buy_price_min'],
                    'buy_price_max': item['buy_price_max'],
                }
                # generate key prefix
                key = generate_cache_key(_item_id, _city, _quality)
                # store in cache
                r.hmset(key, _prices)


def get_item_price_data(item_id: str, city: cities.City = None, quality: int = None):
    def create_key_match_pattern():
        pattern = f'{item_id}:'
        if city:
            pattern += f'{city.value}:'
        else:
            pattern += '*:'
        if quality:
            pattern += f'{quality}'
        else:
            pattern += '*'
        return pattern

    match_pattern = create_key_match_pattern()
    keys = r.keys(match_pattern)

    res = {}
    for key in keys:
        res[key] = r.hgetall(key)
    return res


def find_item_id_by_name(name: str) -> str:
    for item in ITEM_DATA:
        localized_names = item['LocalizedNames']
        if localized_names:
            if localized_names['EN-US'] == name:
                return item['UniqueName']


def generate_item_ids_for_all_enchants(item_id: str = None, name: str = None) -> list:
    if name:
        item_id = find_item_id_by_name(name)
    if item_id:
        return [item_id, item_id + '@1', item_id + '@2', item_id + '@3']
    else:
        raise ValueError(f'No item ids found for name {name} or id {item_id}!')
