import sqlite3
import math

from bot.database import connection, cursor


def create_locations():
    cursor.execute("""INSERT INTO locations (location_id,
                                        x_coord,
                                        y_coord,
                                        location_type,
                                        location_name) 
                                VALUES (
                                          0,
                                          -5,
                                          -5,
                                          'safe',
                                          'capital'
                                          ), 
                                        (
                                          1,
                                          0,
                                          0,
                                          'safe',
                                          'village'), 
                                        (
                                          2,
                                          0,
                                          5,
                                          'fight',
                                          'mountains'
                                        ),
                                        (
                                          3,
                                          5,
                                          0,
                                          'fight',
                                          'jungle'
                                        )""")

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (0,
                                        1,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 0,
                    'to_location_id': 1,
                    'to_location_name': 'village',
                    'distance': math.sqrt(5**2 + 5**2)})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 1,
                    'to_location_id': 0,
                    'to_location_name': 'capital',
                    'distance': math.sqrt(5**2 + 5**2)})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 1,
                    'to_location_id': 2,
                    'to_location_name': 'mountains',
                    'distance': 5})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 2,
                    'to_location_id': 1,
                    'to_location_name': 'village',
                    'distance': 5})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 1,
                    'to_location_id': 3,
                    'to_location_name': 'jungle',
                    'distance': 5})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 3,
                    'to_location_id': 1,
                    'to_location_name': 'village',
                    'distance': 5})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 2,
                    'to_location_id': 3,
                    'to_location_name': 'jungle',
                    'distance': math.sqrt(5**2 + 5**2)})

    cursor.execute("""INSERT INTO location_connections (from_location_id,
                                        to_location_id,
                                        to_location_name,
                                        distance) 
                                VALUES (:from_location_id,
                                        :to_location_id,
                                        :to_location_name,
                                        :distance)""",
                   {'from_location_id': 3,
                    'to_location_id': 2,
                    'to_location_name': 'mountains',
                    'distance': math.sqrt(5**2 + 5**2)})

    connection.commit()


def create_items():
    cursor.execute("""INSERT INTO items (item_name,
                                        cost,
                                        cost_to_sale,
                                        item_type,
                                        hp,
                                        mana,
                                        attack,
                                        magic_attack,
                                        armour,
                                        magic_armour,
                                        req_level,
                                        item_id,
                                        available_capital,
                                        available_village) 
                                VALUES (
                                          'clarity',
                                          15,
                                          10,
                                          'potion',
                                          0,
                                          50,
                                          0,
                                          0,
                                          0,
                                          0,
                                          0,
                                          0,
                                          1,
                                          1
                                          ), 

                                        (
                                          'healing salve',
                                          15,
                                          10,
                                          'potion',
                                          50,
                                          0,
                                          0,
                                          0,
                                          0,
                                          0,
                                          0,
                                          1,
                                          1,
                                          1
                                          ),

                                        (
                                          'shield',
                                          50,
                                          40,
                                          'item',
                                          0,
                                          0,
                                          0,
                                          0,
                                          15,
                                          15,
                                          3,
                                          2,
                                          1,
                                          0
                                          ),
                                        
                                        (
                                          'magic stick',
                                          120,
                                          40,
                                          'item',
                                          0,
                                          20,
                                          0,
                                          50,
                                          0,
                                          0,
                                          5,
                                          3,
                                          1,
                                          0
                                          )""")

    connection.commit()


def create_mobs():
    cursor.execute("""INSERT INTO mobs (mob_name,
                                        mob_id,
                                        hp,
                                        xp,
                                        money,
                                        req_level,
                                        attack_type,
                                        attack,
                                        armour,
                                        magic_armour) 
                                VALUES (
                                          'harpy',
                                          1,
                                          30,
                                          30,
                                          30,
                                          0,
                                          'regular',
                                          10,
                                          0,
                                          0
                                        ), 

                                        (
                                          'centaur',
                                          2,
                                          100,
                                          50,
                                          50,
                                          3,
                                          'regular',
                                          15,
                                          10,
                                          5
                                        ),

                                        (
                                          'wizard',
                                          3,
                                          70,
                                          70,
                                          70,
                                          5,
                                          'magic',
                                          30,
                                          0,
                                          20
                                        )""")

    connection.commit()


def create_bd():
    create_locations()
    create_items()
    create_mobs()
