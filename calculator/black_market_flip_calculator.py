import cities
import datafetch


# TODO: Fix this all.

def find_max_profits(min_profit: int = 1000):
	profits = {}
	for item in datafetch.ITEM_DATA:
		item_id = item['UniqueName']
		car_prices = datafetch.get_item_price_data(item_id, cities.City.Caerleon)
		bm_prices = datafetch.get_item_price_data(item_id, cities.City.Black_Market)

		buy_prices, sell_prices = [], []
		for k, car_price in car_prices.items():
			bm_key = k.replace('Caerleon', 'Black Market')
			if bm_key in bm_prices:
				bm_price = bm_prices[bm_key]
				buy_prices.append(int(car_price['sell_price_min']))
				sell_prices.append(int(bm_price['sell_price_min']))

		buy_index, best_profit = 0, 0
		for i, v in enumerate(buy_prices):
			if v < buy_prices[buy_index]:
				buy_index = i

		for i in range(buy_index):
			profit = sell_prices[i] - buy_prices[buy_index]
			if profit >= min_profit:
				key = item['LocalizedNames']['EN-US']
				if '@' in item_id:
					key += '@' + item_id.split('@')[1]
				profits[key] = profit

	return {k: v for k, v in sorted(profits.items(), key=lambda x: x[1], reverse=True)}


def find_max_instant_profits(min_profit: int = 1000):
	profits = {}
	for item in datafetch.ITEM_DATA:
		item_id = item['UniqueName']
		car_prices = datafetch.get_item_price_data(item_id, cities.City.Caerleon)
		bm_prices = datafetch.get_item_price_data(item_id, cities.City.Black_Market)

		buy_prices, sell_prices = [], []
		for k, car_price in car_prices.items():
			bm_key = k.replace('Caerleon', 'Black Market')
			if bm_key in bm_prices:
				bm_price = bm_prices[bm_key]
				buy_prices.append(int(car_price['sell_price_min']))
				sell_prices.append(int(bm_price['buy_price_max']))

		buy_index, best_profit = 0, 0
		for i, v in enumerate(buy_prices):
			if v < buy_prices[buy_index]:
				buy_index = i

		for i in range(buy_index):
			profit = sell_prices[i] - buy_prices[buy_index]
			if profit >= min_profit:
				key = item['LocalizedNames']['EN-US']
				if '@' in item_id:
					key += '@' + item_id.split('@')[1]
				profits[key] = profit

	return {k: v for k, v in sorted(profits.items(), key=lambda x: x[1], reverse=True)}
