from asyncio import sleep

from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.types.update import AllowedUpdates
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from bot.misc import TgKeys
from bot.misc.util import get_command_text

from bot.database.methods.create import create_bd
from bot.database.methods.get import is_created_hero_bd, is_in_safe_zone_bd, is_fighting_hero_bd, get_hero_name_bd, get_hero_info_bd
from bot.database.methods.update import create_hero_bd, delete_hero_bd, refresh_hero_bd
from bot.database.methods.location import get_hero_location_id_bd, get_hero_available_locations_bd, get_location_id_bd, get_distance_bd, set_hero_location_bd
from bot.database.methods.item import get_hero_items_bd, get_hero_gear_bd, get_hero_available_items_bd, get_item_info_bd, buy_item_bd, sell_item_bd, use_item_bd, take_off_item_bd
from bot.database.methods.fight import create_mob_bd, delete_mob_bd, hit_mob_bd, hits_taken_bd


bot = Bot(token=TgKeys.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """
    Starting Lota game
    """
    await message.reply("YOURE ABOUT TO ENTER LOTA GAME\n\n"
                        "GL HF")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """
    Getting command list
    """
    await message.reply("/help TO GET COMMAND LIST\n\n"
                        "/create_hero <name> TO CREATE NEW HERO\n\n"
                        "/delete_hero TO DELETE HERO\n\n"
                        "/check_hero TO CHECK HERO INFO\n\n"
                        "/check_inventoty TO CHECK HERO INVENTORY\n\n"
                        "/check_gear TO CHECK HERO GEAR\n\n"
                        "/check_locations TO SEE REACHABLE LOCATIONS\n\n"
                        "/move <location name> TO CHANGE LOCATION\n\n"
                        "/check_shop TO SEE AVAILABLE ITEMS IN LOCATION'S SHOP\n\n"
                        "/check_item <name> TO SEE ITEM/POTION INFORMATION\n\n"
                        "/buy <name> TO BUY ITEM/POTION\n\n"
                        "/sell <name> TO SELL ITEM/POTION\n\n"
                        "/use <name> TO USE ITEM/POTION\n\n"
                        "/take_off <name> TO TAKE OFF ITEM\n\n"
                        "/fight TO START FIGHT\n\n"
                        "/hit TO HIT MOB WHILE FIGHTING\n\n")


@dp.message_handler(commands=['create_hero'])
async def create_hero(message: types.Message):
    """
    Creating hero, only one hero can be ctreted per user
    """
    if is_created_hero_bd(message.from_user.id):
        await message.reply(f'NEW HERO CANT BE CREATED AS YOU HAVE ALREADY GOT ONE')
        return

    hero_name = get_command_text(message.text)

    if not hero_name:
        await message.reply(f'INVALID HERO NAME, PLEASE TRY AGAIN')
        return

    create_hero_bd(message.from_user.id, hero_name)
    await message.reply(f'HERO {hero_name} WAS CREATED')


@dp.message_handler(commands=['delete_hero'])
async def delete_hero(message: types.Message):
    """
    Deleting hero
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO DELETE')
        return

    hero_name = delete_hero_bd(message.from_user.id)

    if not hero_name:
        await message.reply(f'SOMETHING WENT WRONG, TRY AGAIN\n\n')
        return

    await message.reply(f'HERO {hero_name} WAS DELETED\n\n')


@dp.message_handler(commands=['check_hero'])
async def check_hero(message: types.Message):
    """
    Checking hero info
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK INFO')
        return

    hero_info = get_hero_info_bd(message.from_user.id)

    if not hero_info:
        await message.reply(f'NO HERO INFO, TRY AGAIN\n\n')
        return

    await message.reply(hero_info)


@dp.message_handler(commands=['check_inventoty'])
async def check_hero_inventoty(message: types.Message):
    """
    Checking hero inventory
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK INVENTORY')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    hero_items = get_hero_items_bd(message.from_user.id)

    if not hero_items:
        await message.reply(f'YOUR INVENTORY IS EMPTY\n\n')
        return

    hero_items_message = "YOUR INVENTORY:\n\n"
    for item in hero_items.items():
        hero_items_message += f'{item[0]} {item[1]}\n'
    await message.reply(hero_items_message)


@dp.message_handler(commands=['check_gear'])
async def check_hero_gear(message: types.Message):
    """
    Checking hero gear
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK GEAR')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    hero_gear = get_hero_gear_bd(message.from_user.id)

    if not hero_gear:
        await message.reply(f'YOU HAVE NO GEAR\n\n')
        return

    hero_gear_message = "YOUR GEAR:\n\n"
    for item in hero_gear:
        hero_gear_message += f'{item[0]}\n'
    await message.reply(hero_gear_message)


@dp.message_handler(commands=['check_locations'])
async def check_hero_locations(message: types.Message):
    """
    Checking hero available locations
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK LOCATIONS')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    if is_fighting_hero_bd(message.from_user.id):
        await message.reply(f'YOU ARE NOW FIGHTING... TRY AGAIN LATER\n\n')
        return

    available_locations = get_hero_available_locations_bd(message.from_user.id)

    if not available_locations:
        await message.reply(f'NO HERO LOCATION, TRY AGAIN\n\n')
        return

    available_locations_message = "YOU CAN MOVE TO:\n\n"
    for location in available_locations:
        available_locations_message += f'{location}\n'
    await message.reply(available_locations_message)


@dp.message_handler(commands=['move'])
async def move_hero(message: types.Message):
    """
    Moving hero to available location
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO MOVE')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    if is_fighting_hero_bd(message.from_user.id):
        await message.reply(f'YOU ARE NOW FIGHTING... TRY AGAIN LATER\n\n')
        return

    to_location_name = get_command_text(message.text)
    if not to_location_name in get_hero_available_locations_bd(message.from_user.id):
        await message.reply(f'NO MOVEMNT WAS MADE, TRY AGAIN\n\n')
        return

    to_location_id = get_location_id_bd(to_location_name)
    distance = get_distance_bd(get_hero_location_id_bd(
        message.from_user.id), to_location_id)

    await message.reply(f'YOU ARE NOW TRAVVELING TO {to_location_name}')

    set_hero_location_bd(message.from_user.id, -1)
    await sleep(distance)
    set_hero_location_bd(message.from_user.id, to_location_id)

    if is_in_safe_zone_bd(message.from_user.id):
        refresh_hero_bd(message.from_user.id)

    await message.reply(f'YOU ARRIVED TO {to_location_name}')


@dp.message_handler(commands=['check_shop'])
async def check_shop(message: types.Message):
    """
    Checking availabe items in shop
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK SHOP')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    if is_fighting_hero_bd(message.from_user.id):
        await message.reply(f'YOU ARE NOW FIGHTING... TRY AGAIN LATER\n\n')
        return

    available_items = get_hero_available_items_bd(message.from_user.id)

    if not available_items:
        await message.reply(f'NO ITEMS AVAILABLE...\n\n')
        return

    available_items_message = "SHOP ITEMS:\n\n"
    for item in available_items:
        available_items_message += f'{item}\n'
    await message.reply(available_items_message)


@dp.message_handler(commands=['check_item'])
async def check_item(message: types.Message):
    """
    Checking item information
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK ITEM INFO')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    item_name = get_command_text(message.text)
    item_info = get_item_info_bd(item_name)

    if not item_info:
        await message.reply(f'NO SUCH ITEM\n\n')
        return

    await message.reply(item_info)


@dp.message_handler(commands=['buy'])
async def buy_item(message: types.Message):
    """
    Buy item
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK ITEM INFO')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    if is_fighting_hero_bd(message.from_user.id):
        await message.reply(f'YOU ARE NOW FIGHTING... TRY AGAIN LATER\n\n')
        return

    item_name = get_command_text(message.text)

    if not item_name in get_hero_available_items_bd(message.from_user.id):
        await message.reply(f'NO SUCH ITEM\n\n')
        return

    await message.reply(buy_item_bd(item_name, message.from_user.id))


@dp.message_handler(commands=['sell'])
async def sell_item(message: types.Message):
    """
    Sell item
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO CHECK ITEM INFO')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    if is_fighting_hero_bd(message.from_user.id):
        await message.reply(f'YOU ARE NOW FIGHTING... TRY AGAIN LATER\n\n')
        return

    item_name = get_command_text(message.text)

    if not item_name in get_hero_items_bd(message.from_user.id):
        await message.reply(f'NO SUCH ITEM\n\n')
        return

    if not item_name in get_hero_available_items_bd(message.from_user.id):
        await message.reply(f'ITEM CAN BE SOLD ONLY WHERE IT CAN BE BOUGHT\n\n')
        return

    await message.reply(sell_item_bd(item_name, message.from_user.id))


@dp.message_handler(commands=['use'])
async def use_item(message: types.Message):
    """
    Use item
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO USE ITEM')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    item_name = get_command_text(message.text)

    if not item_name in get_hero_items_bd(message.from_user.id):
        await message.reply(f'NO SUCH ITEM\n\n')
        return

    await message.reply(use_item_bd(item_name, message.from_user.id))


@dp.message_handler(commands=['take_off'])
async def take_off_item(message: types.Message):
    """
    Take off item
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO TAKE OFF ITEM')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    item_name = get_command_text(message.text)

    if not item_name in get_hero_items_bd(message.from_user.id):
        await message.reply(f'NO SUCH ITEM\n\n')
        return

    await message.reply(take_off_item_bd(item_name, message.from_user.id))


@dp.message_handler(commands=['fight'])
async def start_fight(message: types.Message):
    """
    Starting fight
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO START FIGHT')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    await message.reply(create_mob_bd(message.from_user.id))

    while is_fighting_hero_bd(message.from_user.id):
        hits_taken = hits_taken_bd(message.from_user.id)
        await sleep(60)
        hits_taken_update = hits_taken_bd(message.from_user.id)

        if hits_taken_update == hits_taken:
            hero_name = get_hero_name_bd(message.from_user.id)
            delete_mob_bd(message.from_user.id)
            delete_hero_bd(message.from_user.id)
            create_hero_bd(message.from_user.id, hero_name)
            await message.reply(f'HERO WAS KILLED IN FIGHT... RESTARTING LOTA GAME\n\n')
            return


@dp.message_handler(commands=['hit'])
async def hit(message: types.Message):
    """
    Hit mob while fighting
    """
    if not is_created_hero_bd(message.from_user.id):
        await message.reply(f'NO HERO TO HIT MOB')
        return

    if get_hero_location_id_bd(message.from_user.id) == -1:
        await message.reply(f'YOU ARE NOW TRAVVELING... TRY AGAIN LATER\n\n')
        return

    if not is_fighting_hero_bd(message.from_user.id):
        await message.reply(f'YOU ARE NOT FIGHTING NOW... TRY AGAIN LATER\n\n')
        return

    await message.reply(hit_mob_bd(message.from_user.id))


async def __on_start_up(dp: Dispatcher) -> None:
    create_bd()
    pass


def start_bot():
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
