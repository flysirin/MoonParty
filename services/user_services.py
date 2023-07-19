from bot_object import bot_object
from models.methods import get_user_data, update_user_data, set_user_data
from config_data.config import ADMIN_IDS
from aiogram import Bot
from keyboards import user_keyboards


async def get_active_rooms():
    main_admin_id = int(ADMIN_IDS.split(',')[0])
    data = await get_user_data(bot=bot_object, user_id=main_admin_id)
    hosts = data.get('hosts', {})

    active_leaders = dict()
    for nickname, user_data in hosts.items():
        if user_data.get('user_id', {}):
            active_leaders.update({nickname: user_data.get('user_id')})

    active_rooms = dict()
    for nickname, user_id in active_leaders.items():
        data_form_leader = await get_user_data(bot=bot_object, user_id=user_id)
        room_name = data_form_leader.get('room_name', None)
        if data_form_leader.get('active_registration', False):
            active_rooms.update({room_name: user_id})
    return active_rooms


async def register_user_in_room(username: str = None, user_id: int = None, host_id: int = None):
    players = (await get_user_data(bot=bot_object, user_id=host_id)).get('players', {})
    if not players:
        await update_user_data(bot=bot_object, user_id=host_id, data={'players': {}})

    cur_user_number = await _get_next_number(players=players)
    player = {user_id: {'nickname': username, 'role': None, 'lives': 10,
                        'is_werewolf': False, 'is_change_role': False, 'is_speaker': False,
                        'who_clinked_role': [], 'user_number': cur_user_number}}
    players.update(player)
    await update_user_data(bot=bot_object, user_id=host_id, data={'players': players})
    return cur_user_number


async def _get_next_number(players: dict):
    user_numbers = {number.get('user_number', 0) for number in players.values()}
    cur_user_number = 1
    while cur_user_number in user_numbers:
        cur_user_number += 1
    return cur_user_number


async def send_info_to_user(host_id: int, user_id: int, bot: Bot):
    if not host_id:
        return


async def send_info_to_users(host_id: int, bot: Bot):
    players = (await get_user_data(bot, host_id)).get('players', {})
    players_info = await _get_users_info(host_id=host_id, bot=bot)

    for player_id in players:
        await bot.send_message(text=players_info, chat_id=player_id,
                               reply_markup=user_keyboards.user_game_kb(),
                               disable_notification=True)


async def _get_users_info(host_id: int, bot: Bot):
    leader_data = await get_user_data(bot, host_id)
    players = leader_data.get('players', {})
    players_info = ''
    for player_id, player_data in players.items():
        players_info += f"{player_data.get('nickname', 0)} | " \
                        f"lives:  {[0, player_data.get('lives', 0)][player_data.get('lives', 0) > 0]} | " \
                        f"{['', 'Speaker'][leader_data.get('current_speaker', 0) == player_id]}\n"
    return players_info


async def update_user_nickname(user_id: int, bot: Bot, nickname: str):
    host_id = (await get_user_data(bot=bot, user_id=user_id)).get('select_host_id', 0)
    if not host_id:
        return
    leader_data = await get_user_data(bot=bot, user_id=host_id)
    if leader_data.get('players', {}).get(user_id, 0):
        leader_data['players'][user_id]['nickname'] = nickname
        await update_user_data(bot=bot, user_id=host_id, data=leader_data)


# async def get_user_id_by_serial_number(host_id: int, serial_number: int):
#     players = (await get_data_from_user(bot_object, host_id)).get('players', {})
#     for player_id, player_data in players.items():
#         if player_data.get('user_number', 0):
#             return player_id
#     return False
