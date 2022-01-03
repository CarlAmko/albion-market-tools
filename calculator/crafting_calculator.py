FOCUS_PER_DAY = 10000


def calculate_focus_cost(base_cost: int, focus_efficiency: int) -> int:
	return int(base_cost / 2 ** (focus_efficiency / 10000))


def calculate_total_craft_quantity(base_amount: int, return_rate: float) -> int:
	total = base_amount
	while base_amount > 0:
		base_amount = round(return_rate * base_amount)
		total += base_amount
	return total


def calculate_focus_crafts_per_day(base_focus_cost: int, focus_efficiency: int, focus_return_rate: float) -> int:
	focus_cost = calculate_focus_cost(base_focus_cost, focus_efficiency)
	return calculate_total_craft_quantity(FOCUS_PER_DAY // focus_cost, focus_return_rate)



if __name__ == '__main__':
	# print(calculate_focus_cost(, 7500))
	print(calculate_total_craft_quantity(100, 0.453))
