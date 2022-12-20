import sqlite3
from bot.database import connection, cursor

from bot.database.methods.location import get_hero_location_id_bd


def get_hero_items_bd(user_id):

    cursor.execute("""SELECT item_name,
                             quantity
                    FROM carry_items
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_items_names = cursor.fetchall()

    hero_items = dict()
    for item in hero_items_names:
        hero_items[item[0]] = item[1]

    return hero_items


def get_hero_gear_bd(user_id):

    cursor.execute("""SELECT item_name,
                             quantity
                    FROM carry_items
                    WHERE telegram_id = :telegram_id
                    AND is_carried = :is_carried""",
                   {'telegram_id': user_id,
                    'is_carried': 1})

    hero_gear_names = cursor.fetchall()

    hero_gear = list()
    for item in hero_gear_names:
        hero_gear.append(item[0])

    return hero_gear


def get_hero_available_items_bd(user_id):
    hero_location_id = get_hero_location_id_bd(user_id)

    if hero_location_id == 0:
        cursor.execute("""SELECT item_name
                    FROM items
                    WHERE available_capital = 1""")
    elif hero_location_id == 1:
        cursor.execute("""SELECT item_name
                    FROM items
                    WHERE available_village = 1""")

    available_items_names = cursor.fetchall()

    available_items = list()
    for item in available_items_names:
        available_items.append(item[0])

    return available_items


def get_item_info_bd(item_name):

    cursor.execute("""SELECT cost,
                            cost_to_sale,
                            item_type,
                            hp,
                            mana,
                            attack,
                            magic_attack,
                            armour,
                            magic_armour,
                            req_level,
                            available_capital,
                            available_village
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_info = cursor.fetchone()

    if item_info:
        available_capital = "YES" if item_info[10] else "NO"
        available_village = "YES" if item_info[11] else "NO"
        item_info = (f"COST: {item_info[0]}\n\n"
                     f"SALE COST: {item_info[1]}\n\n"
                     f"TYPE: {item_info[2]}\n\n"
                     f"HP: {item_info[3]}\n\n"
                     f"MANA: {item_info[4]}\n\n"
                     f"ATTACK: {item_info[5]}\n\n"
                     f"MAGIC ATTACK: {item_info[6]}\n\n"
                     f"ARMOUR: {item_info[7]}\n\n"
                     f"MAGIC ARMOUR: {item_info[8]}\n\n"
                     f"REQUIRED LEVEL: {item_info[9]}\n\n"
                     f"AVAILABE IN CAPITAL: {available_capital}\n\n"
                     f"AVAILABE IN VILLAGE: {available_village}\n\n")

        return item_info
    else:
        return None


def get_item_id_bd(item_name):
    cursor.execute("""SELECT item_id
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_id = cursor.fetchone()

    if item_id:
        return int(item_id[0])
    else:
        return None


def get_hero_money(user_id):
    cursor.execute("""SELECT money
                    FROM users
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    money = cursor.fetchone()

    if not money:
        return None

    return int(money[0])


def set_hero_money(money, user_id):
    cursor.execute("""UPDATE users 
                    SET money = :money
                    WHERE telegram_id = :telegram_id""",
                   {'money': money,
                    'telegram_id': user_id})

    connection.commit()


def get_item_quantity(user_id, item_name):
    cursor.execute("""SELECT quantity
                    FROM carry_items
                    WHERE telegram_id = :telegram_id
                    AND item_name = :item_name""",
                   {'telegram_id': user_id,
                    'item_name': item_name})

    quantity = cursor.fetchone()

    if not quantity:
        return 0
    else:
        return int(quantity[0])


def buy_item_bd(item_name, user_id):
    cursor.execute("""SELECT cost
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_cost = cursor.fetchone()

    if not item_cost:
        return None

    item_cost = int(item_cost[0])

    money = get_hero_money(user_id)

    if money is None:
        return None

    if item_cost > money:
        return "YOU DONT HAVE ENOUGH MONEY TO BUY"

    money -= item_cost

    quantity = get_item_quantity(user_id, item_name)

    if quantity:
        cursor.execute("""UPDATE carry_items 
                    SET quantity = :quantity
                    WHERE telegram_id = :telegram_id""",
                       {'quantity': quantity + 1,
                        'telegram_id': user_id})
    else:
        cursor.execute("""INSERT INTO carry_items (telegram_id,
                                        item_id,
                                        item_name,
                                        is_carried,
                                        quantity) 
                                VALUES (:telegram_id,
                                        :item_id,
                                        :item_name,
                                        :is_carried,
                                        :quantity)""",
                       {'telegram_id': user_id,
                        'item_id': get_item_id_bd(item_name),
                        'item_name': item_name,
                        'is_carried': 0,
                        'quantity': 1})

    connection.commit()

    set_hero_money(money, user_id)

    return (f"AVAILABLE MONEY: {money}\n\n"
            f"YOU NOW HAVE: {quantity + 1} {item_name}(s)")


def sell_item_bd(item_name, user_id):
    cursor.execute("""SELECT cost_to_sale
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_cost_to_sale = cursor.fetchone()

    if not item_cost_to_sale:
        return None

    item_cost_to_sale = int(item_cost_to_sale[0])

    money = get_hero_money(user_id)

    if money is None:
        return None

    money += item_cost_to_sale

    quantity = get_item_quantity(user_id, item_name)

    if quantity == 1:
        cursor.execute("""DELETE FROM carry_items 
                    WHERE telegram_id = :telegram_id
                    AND item_name = :item_name""",
                       {'telegram_id': user_id,
                        'item_name': item_name})
    else:
        cursor.execute("""UPDATE carry_items 
                    SET quantity = :quantity
                    WHERE telegram_id = :telegram_id""",
                       {'quantity': quantity - 1,
                        'telegram_id': user_id})

    connection.commit()

    set_hero_money(money, user_id)

    return (f"AVAILABLE MONEY: {money}\n\n"
            f"YOU NOW HAVE: {quantity - 1} {item_name}(s)")


def get_item_type(item_name):
    cursor.execute("""SELECT item_type
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_type = cursor.fetchone()

    if item_type:
        return item_type[0]
    else:
        return None


def use_item_bd(item_name, user_id):
    cursor.execute("""SELECT hp,
                            current_hp,
                            mana,
                            current_mana,
                            attack,
                            magic_attack,
                            armour,
                            magic_armour
                    FROM users
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_info = cursor.fetchone()

    cursor.execute("""SELECT hp,
                            mana,
                            attack,
                            magic_attack,
                            armour,
                            magic_armour
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_info = cursor.fetchone()

    item_type = get_item_type(item_name)

    if not item_info or not hero_info or item_type is None:
        return None

    if item_type == 'item':
        cursor.execute("""UPDATE users 
                    SET hp = :hp,
                        current_hp = :current_hp,
                        mana = :mana,
                        current_mana = :current_mana,
                        attack = :attack,
                        magic_attack = :magic_attack,
                        armour = :armour,
                        magic_armour = :magic_armour
                    WHERE telegram_id = :telegram_id""",
                       {'hp': int(hero_info[0]) + int(item_info[0]),
                        'current_hp': int(hero_info[1]) + int(item_info[0]),
                        'mana': int(hero_info[2]) + int(item_info[1]),
                        'current_mana': int(hero_info[3]) + int(item_info[1]),
                        'attack': int(hero_info[4]) + int(item_info[2]),
                        'magic_attack': int(hero_info[5]) + int(item_info[3]),
                        'armour': int(hero_info[6]) + int(item_info[4]),
                        'magic_armour': int(hero_info[7]) + int(item_info[5]),
                        'telegram_id': user_id})

        connection.commit()

        return f"GEAR IS UPDATED, CHECK NEW HERO INFO"

    if item_type == 'potion':
        cursor.execute("""UPDATE carry_items 
                    SET current_hp = :current_hp,
                        current_mana = :current_mana
                    WHERE telegram_id = :telegram_id""",
                       {'current_hp': max(int(hero_info[0]), int(hero_info[1]) + int(item_info[0])),
                        'current_mana': max(int(hero_info[2]), int(hero_info[3]) + int(item_info[1])),
                        'telegram_id': user_id})

        connection.commit()
        return f"POTION IS USED, CHECK NEW HERO INFO"


def take_off_item_bd(item_name, user_id):
    item_type = get_item_type(item_name)

    if item_type is None:
        return None

    if item_type == 'item':
        cursor.execute("""SELECT hp,
                            current_hp,
                            mana,
                            current_mana,
                            attack,
                            magic_attack,
                            armour,
                            magic_armour
                    FROM users
                    WHERE telegram_id = :telegram_id""",
                       {'telegram_id': user_id})

    hero_info = cursor.fetchone()

    cursor.execute("""SELECT hp,
                            mana,
                            attack,
                            magic_attack,
                            armour,
                            magic_armour
                    FROM items
                    WHERE item_name = :item_name""",
                   {'item_name': item_name})

    item_info = cursor.fetchone()

    item_type = get_item_type(item_name)

    if not item_info or not hero_info or item_type is None:
        return None

    if item_type == 'item':
        cursor.execute("""UPDATE users 
                    SET hp = :hp,
                        current_hp = :current_hp,
                        mana = :mana,
                        current_mana = :current_mana,
                        attack = :attack,
                        magic_attack = :magic_attack,
                        armour = :armour,
                        magic_armour = :magic_armour
                    WHERE telegram_id = :telegram_id""",
                       {'hp': int(hero_info[0]) - int(item_info[0]),
                        'current_hp': max(0, int(hero_info[1]) - int(item_info[0])),
                        'mana': int(hero_info[2]) - int(item_info[1]),
                        'current_mana': max(0, int(hero_info[3]) - int(item_info[1])),
                        'attack': int(hero_info[4]) - int(item_info[2]),
                        'magic_attack': int(hero_info[5]) - int(item_info[3]),
                        'armour': int(hero_info[6]) - int(item_info[4]),
                        'magic_armour': int(hero_info[7]) - int(item_info[5]),
                        'telegram_id' : user_id})

        connection.commit()

        return f"GEAR IS TAKEN OFF, CHECK NEW HERO INFO"

    if item_type == 'potion':
        return f"ONLY ITEMS CAN BE TAKEN OFF"
