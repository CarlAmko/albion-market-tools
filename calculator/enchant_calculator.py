import data.prefix as prefix
import datafetch


def get_items_required_for_enchant(item_id: str):
    if prefix.is_shoe(item_id) or prefix.is_head(item_id):
        return 48
    elif prefix.is_armor(item_id):
        return 96
    elif prefix.is_1h(item_id):
        return 144
    elif prefix.is_2h(item_id):
        return 196


def get_rune_prices(tier: int, city: str):
    def create_rune_name(pre: str):
        return pre + "'s Rune"

    _prefix = prefix.TIER_PREFIXES[tier]
    if _prefix:
        rune_id = datafetch.find_item_id_by_name(create_rune_name(_prefix))
        return datafetch.fetch_current_prices(rune_id, city=city)[rune_id]

    return None


def get_soul_prices(tier: int, city: str):
    def create_soul_name(pre: str):
        return pre + "'s Soul"

    _prefix = prefix.TIER_PREFIXES[tier]
    if _prefix:
        soul_id = datafetch.find_item_id_by_name(create_soul_name(_prefix))
        return datafetch.fetch_current_prices(soul_id, city=city)[soul_id]

    return None


def get_relic_prices(tier: int, city: str):
    def create_relic_name(pre: str):
        return pre + "'s Relic"

    _prefix = prefix.TIER_PREFIXES[tier]
    if _prefix:
        relic_id = datafetch.find_item_id_by_name(create_relic_name(_prefix))
        return datafetch.fetch_current_prices(relic_id, city=city)[relic_id]

    return None


def calculate_profits_for_item(item_id: str, city: str):
    all_item_ids = datafetch.generate_item_ids_for_all_enchants(item_id=item_id)
    num_enchant_items = get_items_required_for_enchant(item_id)
    prices = []
    for item_id in all_item_ids:
        prices.append(datafetch.fetch_current_prices(item_id, city=city))

    profits = {}
    for i in range(len(prices) - 1):
        base_profit = prices[i + 1][all_item_ids[i + 1]]['sell_price_min'] - prices[i][all_item_ids[i]][
            'sell_price_min']
        tier = prefix.get_tier(item_id)

        # X.0 -> X.1
        if i == 0:
            enchant_cost = get_rune_prices(tier, city=city)
        # X.1 -> X.2
        elif i == 1:
            enchant_cost = get_soul_prices(tier, city=city)
        # X.2 -> X.3
        elif i == 2:
            enchant_cost = get_relic_prices(tier, city=city)
        else:
            raise ValueError("Somehow trying to enchant beyond 3??")

        profits[all_item_ids[i]] = base_profit - (enchant_cost['sell_price_min'] * num_enchant_items)

    return profits


# TODO: This is expensive... add hourly caching here.
def find_best_enchants(city: str, limit: int = 20):
    # FIXME: Only checking equipment for now
    for item in datafetch.ITEM_DATA:
        # Only look at base enchant item so we can force a particular order
        unique_name = item['UniqueName']
        if '@' not in unique_name:
            calculate_profits_for_item(unique_name, city=city)
