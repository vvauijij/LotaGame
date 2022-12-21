import sqlite3

from random import randint

from bot.database import connection, cursor
from bot.database.methods.get import get_hero_name_bd
from bot.database.methods.update import create_hero_bd, delete_hero_bd


def create_mob_bd(user_id):
    cursor.execute("""SELECT level 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_level = cursor.fetchone()

    cursor.execute("""SELECT mob_name,
                             mob_id,
                             hp,
                             xp,
                             money,
                             req_level,
                             attack_type,
                             attack,
                             armour,
                             magic_armour
                    FROM mobs""")

    mobs = cursor.fetchall()

    if not mobs:
        return f"NO MOBS TO FIGHT..."

    available_mobs = list()
    for mob in mobs:
        if int(mob[5]) <= int(hero_level[0]):
            available_mobs.append(mob)

    if not available_mobs:
        return f"NO MOBS TO FIGHT..."

    random_mob = available_mobs[randint(0, len(available_mobs) - 1)]

    cursor.execute("""UPDATE users 
                    SET is_fighting = :is_fighting
                    WHERE telegram_id = :telegram_id""",
                   {'is_fighting': int(random_mob[1]),
                    'telegram_id': user_id})

    cursor.execute("""INSERT INTO active_mobs (mob_name,
                                               telegram_id,
                                               hp,
                                               xp,
                                               money,
                                               attack_type,
                                               attack,
                                               armour,
                                               magic_armour,
                                               hits_taken) 
                                VALUES (:mob_name,
                                        :telegram_id,
                                        :hp,
                                        :xp,
                                        :money,
                                        :attack_type,
                                        :attack,
                                        :armour,
                                        :magic_armour,
                                        :hits_taken)""",
                   {'mob_name': random_mob[0],
                    'telegram_id': user_id,
                    'hp': int(random_mob[2]),
                    'xp': int(random_mob[3]),
                    'money': int(random_mob[4]),
                    'attack_type': random_mob[6],
                    'attack': int(random_mob[7]),
                    'armour': int(random_mob[8]),
                    'magic_armour': int(random_mob[9]),
                    'hits_taken': 0})

    connection.commit()

    return (f"YOU ARE NOW FIGHTING {random_mob[0]}\n\n"
            f"YOU HAVE A MINUTE TO ATTACK IT")


def delete_mob_bd(user_id):
    cursor.execute("""DELETE FROM active_mobs 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    connection.commit()


def hit_mob_bd(user_id):
    cursor.execute("""SELECT mob_name,
                            hp,
                            xp,
                            money,
                            attack_type,
                            attack,
                            armour,
                            magic_armour,
                            hits_taken
                    FROM active_mobs 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    mob = cursor.fetchone()
    if not mob:
        return None

    cursor.execute("""SELECT level,
                            current_hp,
                            xp,
                            money,
                            attack,
                            magic_attack,
                            armour,
                            magic_armour
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero = cursor.fetchone()
    if not hero:
        return None

    response = ""

    current_mob_hp = int(mob[1]) - max(0, int(hero[4]) -
                                       int(mob[6])) - max(0, int(hero[5]) - int(mob[7]))
    if current_mob_hp <= 0:
        cursor.execute("""UPDATE users 
                    SET is_fighting = :is_fighting
                    WHERE telegram_id = :telegram_id""",
                       {'is_fighting': 0,
                        'telegram_id': user_id})

        delete_mob_bd(user_id)

        cursor.execute("""UPDATE users 
                    SET level = :level,
                        xp = :xp,
                        money = :money
                    WHERE telegram_id = :telegram_id""",
                       {'level': int(hero[0]) + (int(hero[2]) + int(mob[2])) // 100,
                        'xp': (int(hero[2]) + int(mob[2])) % 100,
                        'money': int(hero[3]) + int(mob[3]),
                        'telegram_id': user_id})

        connection.commit()
        return f"YOU HAVE KILLED {mob[0]}!"

    else:
        cursor.execute("""UPDATE active_mobs 
                    SET hp = :hp
                    WHERE telegram_id = :telegram_id""",
                       {'hp': current_mob_hp,
                        'telegram_id': user_id})

        response += f"{mob[0]} NOW HAS {current_mob_hp} HP\n\n"

    current_hero_hp = int(hero[1])
    if mob[4] == 'regular':
        current_hero_hp -= max(0, int(mob[5]) - int(hero[6]))
    else:
        current_hero_hp -= max(0, int(mob[5]) - int(hero[7]))

    if current_hero_hp <= 0:
        hero_name = get_hero_name_bd(user_id)
        delete_mob_bd(user_id)
        delete_hero_bd(user_id)
        create_hero_bd(hero_name)

        connection.commit()
        return f'HERO WAS KILLED IN FIGHT... RESTARTING LOTA GAME\n\n'

    else:
        cursor.execute("""UPDATE users 
                    SET current_hp = :current_hp
                    WHERE telegram_id = :telegram_id""",
                       {'current_hp': current_hero_hp,
                        'telegram_id': user_id})

        response += f"{mob[0]} ATTACKED BACK: YOU NOW HAVE {current_hero_hp} HP\n\n"

    connection.commit()
    return response


def hits_taken_bd(user_id):
    cursor.execute("""SELECT hits_taken
                    FROM active_mobs 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_name = cursor.fetchone()

    if hero_name:
        return int(hero_name[0])
    else:
        return None
