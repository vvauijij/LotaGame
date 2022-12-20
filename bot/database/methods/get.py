import sqlite3
from bot.database import cursor

from bot.database.methods.location import get_hero_location_name_bd


def is_created_hero_bd(user_id) -> bool:
    cursor.execute("""SELECT hero_name 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    return bool(cursor.fetchall())


def is_fighting_hero_bd(user_id) -> bool:
    cursor.execute("""SELECT is_fighting 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    is_fighting = cursor.fetchone()
    if is_fighting:
        return bool(is_fighting[0])
    else:
        return None


def get_hero_info_bd(user_id) -> str:
    cursor.execute("""SELECT hero_name,
                            level,
                            hp,
                            current_hp,
                            mana,
                            current_mana,
                            money,
                            attack,
                            magic_attack,
                            xp,
                            armour,
                            magic_armour
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_info = cursor.fetchone()

    if hero_info:
        hero_info = (f"HERO NAME: {hero_info[0]}\n\n"
                     f"LEVEL: {hero_info[1]}\n\n"
                     f"MAX HP: {hero_info[2]}\n\n"
                     f"CURRENT HP: {hero_info[3]}\n\n"
                     f"MAX MANA: {hero_info[4]}\n\n"
                     f"CURRENT MANA: {hero_info[5]}\n\n"
                     f"MONEY: {hero_info[6]}\n\n"
                     f"ATTACK: {hero_info[7]}\n\n"
                     f"MAGIC ATTACK: {hero_info[8]}\n\n"
                     f"XP: {hero_info[9]}\n\n"
                     f"ARMOUR: {hero_info[10]}\n\n"
                     f"MAGIC ARMOUR: {hero_info[11]}\n\n"
                     f"LOCATION: {get_hero_location_name_bd(user_id)}\n\n")

        return hero_info
    else:
        return None


def get_hero_name_bd(user_id) -> str:
    cursor.execute("""SELECT hero_name 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_info = cursor.fetchone()

    if hero_info:
        return hero_info[0]
    else:
        return None


def get_hero_location_bd(user_id) -> int:
    cursor.execute("""SELECT location_Id 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_info = cursor.fetchone()

    if hero_info:
        return int(hero_info[0])
    else:
        return None
