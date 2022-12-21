import sqlite3
from bot.database import connection, cursor


from bot.database.methods.get import get_hero_name_bd


def create_hero_bd(user_id, hero_name):
    cursor.execute("""INSERT INTO users (telegram_id,
                                        hero_name,
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
                                        magic_armour,
                                        location_id,
                                        is_fighting) 
                                VALUES (:telegram_id,
                                        :hero_name,
                                        :level,
                                        :hp,
                                        :current_hp,
                                        :mana,
                                        :current_mana,
                                        :money,
                                        :attack,
                                        :magic_attack,
                                        :xp,
                                        :armour,
                                        :magic_armour,
                                        :location_id,
                                        :is_fighting)""",
                   {'telegram_id': user_id,
                    'hero_name': hero_name,
                    'level': 0,
                    'hp': 100,
                    'current_hp': 100,
                    'mana': 100,
                    'current_mana': 100,
                    'money': 100,
                    'attack': 10,
                    'magic_attack': 10,
                    'xp': 0,
                    'armour': 0,
                    'magic_armour': 0,
                    'location_id': 0,
                    'is_fighting': 0})

    connection.commit()


def delete_hero_bd(user_id) -> str:
    hero_name = get_hero_name_bd(user_id)

    cursor.execute("""DELETE FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    cursor.execute("""DELETE FROM carry_items 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    connection.commit()

    return hero_name


def refresh_hero_bd(user_id):
    cursor.execute("""SELECT hp,
                            mana
                    FROM users
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_info = cursor.fetchone()

    if not hero_info:
        return None

    cursor.execute("""UPDATE users 
                    SET current_hp = :current_hp,
                        current_mana = :current_mana
                    WHERE telegram_id = :telegram_id""",
                   {'current_hp': int(hero_info[0]),
                    'current_mana': int(hero_info[1]),
                    'telegram_id': user_id})

    connection.commit()
