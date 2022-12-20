from sqlite3 import connect


connection = connect("lota_base.db")
cursor = connection.cursor()

cursor.execute("""
                  CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  telegram_id INTEGER NOT NULL,
                  hero_name text NOT NULL,
                  level INTEGER NOT NULL,
                  hp INTEGER NOT NULL,
                  current_hp INTEGER NOT NULL,
                  mana INTEGER NOT NULL,
                  current_mana INTEGER NOT NULL,
                  money INTEGER NOT NULL,
                  attack INTEGER NOT NULL,
                  magic_attack INTEGER NOT NULL,
                  xp INTEGER NOT NULL,
                  armour INTEGER NOT NULL,
                  magic_armour INTEGER NOT NULL,
                  location_id INTEGER NOT NULL,
                  is_fighting INTEGER NOT NULL);
                  """)

cursor.execute("""
                  CREATE TABLE IF NOT EXISTS locations (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  location_id INTEGER NOT NULL,
                  x_coord INTEGER NOT NULL,
                  y_coord INTEGER NOT NULL,
                  location_type text NOT NULL,
                  location_name text NOT NULL);
                  """)

cursor.execute("""
                  CREATE TABLE IF NOT EXISTS location_connections (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_location_id INTEGER NOT NULL,
                  to_location_id INTEGER NOT NULL,
                  to_location_name text NOT NULL,
                  distance REAL NOT NULL);
                  """)

cursor.execute("""
                  CREATE TABLE IF NOT EXISTS items (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item_name text NOT NULL,
                  cost INTEGER NOT NULL,
                  cost_to_sale INTEGER NOT NULL,
                  item_type text NOT NULL,
                  hp INTEGER NOT NULL,
                  mana INTEGER NOT NULL,
                  attack INTEGER NOT NULL,
                  magic_attack INTEGER NOT NULL,
                  armour INTEGER NOT NULL,
                  magic_armour INTEGER NOT NULL,
                  req_level INTEGER NOT NULL,
                  item_id INTEGER NOT NULL,
                  available_capital INTEGER NOT NULL,
                  available_village INTEGER NOT NULL);
                  """)

cursor.execute("""
                  CREATE TABLE IF NOT EXISTS carry_items (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  telegram_id INTEGER NOT NULL,
                  item_id INTEGER NOT NULL,
                  item_name text NOT NULL,
                  is_carried INTEGER NOT NULL,
                  quantity INTEGER NOT NULL);
                  """)
