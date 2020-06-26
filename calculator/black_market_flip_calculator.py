import datafetch
import cities


def get_black_market_prices(item_ids: list):
    return datafetch.fetch_current_prices(item_ids, city=cities.City.Black_Market.value)['sell_price_min']


def get_caerleon_market_prices(item_ids: list):
    return datafetch.fetch_current_prices(item_ids, city=cities.City.Caerleon.value)['sell_price_min']


# TODO: This is expensive... add hourly caching here.
def find_max_profits(min_profit: int = 0):
    profits = {}
    item_ids = [item['UniqueName'] for item in datafetch.ITEM_DATA]
    bm_prices = get_black_market_prices(item_ids)
    c_prices = get_caerleon_market_prices(item_ids)

    if len(bm_prices) != len(c_prices):
        raise IndexError("Prices not same length!")

    for item_id, bm_item in bm_prices.items():
        c_item = c_prices[item_id]
        profit = bm_item['sell_price_min'] - c_item['sell_price_min']
        if profit > min_profit:
            profits[item_id] = profit

    return profits
