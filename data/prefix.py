TIER_PREFIXES = {
    1: 'Beginner',
    2: 'Novice',
    3: 'Journeyman',
    4: 'Adept',
    5: 'Expert',
    6: 'Master',
    7: 'Grandmaster',
    8: 'Elder'
}


# The following are based on syntax conventions of item ids.

def is_armor(item_id: str):
    return 'ARMOR' in item_id


def is_head(item_id: str):
    return 'HEAD' in item_id


def is_shoe(item_id: str):
    return 'SHOES' in item_id


def is_1h(item_id: str):
    return '1H' in item_id or 'MAIN' in item_id


def is_2h(item_id: str):
    return '2H' in item_id


def is_weapon(item_id: str):
    return is_1h(item_id) or is_2h(item_id)


def is_equipment(item_id: str):
    return is_armor(item_id) or is_head(item_id) or is_shoe(item_id) or is_weapon(item_id)


def get_tier(item_id: str) -> int:
    if 'T2' in item_id:
        return 2
    elif 'T3' in item_id:
        return 3
    elif 'T4' in item_id:
        return 4
    elif 'T5' in item_id:
        return 5
    elif 'T6' in item_id:
        return 6
    elif 'T7' in item_id:
        return 7
    elif 'T8' in item_id:
        return 8
    else:
        return 1
