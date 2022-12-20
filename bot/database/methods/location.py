import sqlite3
from bot.database import connection, cursor

def is_hero_in_safe_zone_bd(user_id) -> bool:
    cursor.execute("""SELECT location_id 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    location_id = cursor.fetchone()
    if location_id:
        return (int(location_id[0]) in [0, 1])
    else:
        return None

def get_hero_location_id_bd(user_id) -> int:
    cursor.execute("""SELECT location_id 
                    FROM users 
                    WHERE telegram_id = :telegram_id""",
                   {'telegram_id': user_id})

    hero_location = cursor.fetchone()

    if hero_location:
        return int(hero_location[0])
    else:
        return None


def get_hero_location_name_bd(user_id) -> str:
    hero_location_id = get_hero_location_id_bd(user_id)

    if hero_location_id == -1:
        return "travveling"

    cursor.execute("""SELECT location_name 
                    FROM locations 
                    WHERE location_id = :hero_location_id""",
                   {'hero_location_id': hero_location_id})

    hero_location = cursor.fetchone()

    if hero_location:
        return hero_location[0]
    else:
        return None


def get_hero_available_locations_bd(user_id) -> str:
    hero_location_id = get_hero_location_id_bd(user_id)

    cursor.execute("""SELECT to_location_name 
                    FROM location_connections 
                    WHERE from_location_id = :from_location_id""",
                   {'from_location_id': hero_location_id})

    available_locations_names = cursor.fetchall()

    available_locations = list()
    for location in available_locations_names:
        available_locations.append(location[0])

    return available_locations


def get_location_id_bd(location_name):
    cursor.execute("""SELECT location_id 
                    FROM locations 
                    WHERE location_name = :to_location_name""",
                   {'to_location_name': location_name})

    to_location_id = cursor.fetchone()

    if to_location_id:
        return int(to_location_id[0])
    else:
        return None


def get_distance_bd(from_location_id, to_location_id):
    cursor.execute("""SELECT distance 
                    FROM location_connections 
                    WHERE from_location_id = :from_location_id
                    AND  to_location_id = :to_location_id""",
                   {'from_location_id': from_location_id,
                    'to_location_id': to_location_id})

    distance = cursor.fetchone()

    if distance:
        return float(distance[0])
    else:
        return None


def set_hero_location_bd(user_id, location_id):
    cursor.execute("""UPDATE users 
                    SET location_id = :location_id
                    WHERE telegram_id = :telegram_id""",
                   {'location_id': location_id,
                    'telegram_id': user_id})

    connection.commit()
