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
def get_all_prices():
    res = {}
    for item in ITEM_DATA:
        unique_name = item['UniqueName']
        res[unique_name] = get_current_prices(unique_name)
    return res


def get_current_prices(search_text: str, town: str = None):
    search_url = API_BASE_URL + search_text
    # default to '1' quality
    params = {'qualities': 1}
    if town:
        params['locations'] = town
    data = requests.get(search_url, params=params).json()

    prices = {}
    for city_data in data:
        _city = city_data['city']
        _sell_min = city_data['sell_price_min']
        _sell_max = city_data['sell_price_max']
        _buy_min = city_data['buy_price_min']
        _buy_max = city_data['buy_price_max']
        _quality = city_data['quality']
        _prices = {
            'sell_price_min': _sell_min,
            'sell_price_max': _sell_max,
            'buy_price_min': _buy_min,
            'buy_price_max': _buy_max,
        }

        prices[_city] = _prices

    return prices


def find_item_id_by_name(name: str) -> str:
    for item in ITEM_DATA:
        localized_names = item['LocalizedNames']
        if localized_names:
            if localized_names['EN-US'] == name:
                return item['UniqueName']


def generate_item_ids_for_all_enchants(name: str) -> list:
    _item_id = find_item_id_by_name(name)
    if _item_id:
        return [_item_id, _item_id + '@1', _item_id + '@2', _item_id + '@3']
    else:
        return []
