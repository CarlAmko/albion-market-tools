import json

import requests

import towns

API_BASE_URL = 'http://albion-online-data.com/api/v2/stats/prices/'

with open('data/items.json') as _json:
    ITEM_DATA = json.load(_json)


def create_town_price_map():
    res = {}
    for town in towns.Town:
        res[town.value] = {}
    return res


# TODO: This is expensive... add hourly caching here.
def get_all_prices(town: str):
    res = {}
    for item in ITEM_DATA:
        unique_name = item['UniqueName']
        res[unique_name] = get_current_prices(unique_name, town=town)
    return res


def get_current_prices(search_text: str, town: str):
    search_url = API_BASE_URL + search_text
    # default to '1' quality
    params = {'qualities': 1, 'locations': town}
    data = requests.get(search_url, params=params).json()[0]

    _sell_min = data['sell_price_min']
    _sell_max = data['sell_price_max']
    _buy_min = data['buy_price_min']
    _buy_max = data['buy_price_max']
    _quality = data['quality']
    _prices = {
        'sell_price_min': _sell_min,
        'sell_price_max': _sell_max,
        'buy_price_min': _buy_min,
        'buy_price_max': _buy_max,
    }
    return _prices


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
        return []
