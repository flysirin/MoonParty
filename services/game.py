import asyncio
from aiogram import Bot
from random import choice, shuffle, randint
from bot_object import bot_object
from models.methods import get_user_data, update_user_data, set_user_state
from lexicon.lexicon import USER_LEXICON, USER_TIMER
from services.user_services import send_info_to_users


async def start_init_players(host_id: int):
    data = await get_user_data(bot_object, host_id)
    data.update({'who_did_not_speak_ids': []})  # next speakers
    data.update({'who_clinked_this_move_ids': []})
    data.update({'winners': []})
    data.update({'current_speaker': 0})
    players = data.get('players', {})

    count_players = len(players)
    list_roles = await _init_roles(count=count_players)
    for player_id in players:
        current_role = list_roles.pop()
        role, is_werewolf = (current_role, False) if current_role != 'werewolf' else (choice(['wolf', 'human']), True)

        players[player_id]['role'] = role
        players[player_id]['is_werewolf'] = is_werewolf
        players[player_id]['lives'] = 10
        players[player_id]['who_clinked_role'] = []
        players[player_id]['is_change_role'] = False

        data['who_did_not_speak_ids'].append(player_id)
        shuffle(data['who_did_not_speak_ids'])
    data["players"] = players
    await update_user_data(bot_object, host_id, data=data)


async def _init_roles(count: int):
    n = count
    n_werewolf, n_wolf = round(n / 5), round(2 * n / 5)
    n_human = n - n_wolf - n_werewolf
    swap_list = [n_human, n_wolf]
    shuffle(swap_list)
    n_wolf, n_human = swap_list
    list_roles = ['werewolf'] * n_werewolf + ['wolf'] * n_wolf + ['human'] * n_human
    shuffle(list_roles)
    return list_roles


async def _get_player_who_did_not_speak_id(host_id: int):
    data = await get_user_data(bot_object, host_id)
    while data.get('who_did_not_speak_ids', []):
        speaker_id = data['who_did_not_speak_ids'].pop()
        if 0 < data['players'][speaker_id]['lives'] < 20:
            data['current_speaker'] = speaker_id
            data['players'][speaker_id]['is_speaker'] = True
            await update_user_data(bot_object, host_id, data=data)
            return speaker_id
    return False


async def _connect_two_players(host_id: int, speaker_id: int, who_clinked_id: int):
    data = await get_user_data(bot_object, host_id)

    player_who_clinked_role = data['players'][who_clinked_id]['role']
    data['players'][speaker_id]['who_clinked_role'].append(
        player_who_clinked_role)  # add role, who clinked with speaker

    if data['players'][speaker_id]['role'] == player_who_clinked_role:
        data['players'][who_clinked_id]['lives'] += 2
    else:
        data['players'][who_clinked_id]['lives'] -= 2
    data['who_clinked_this_move_ids'].append(who_clinked_id)
    await update_user_data(bot_object, host_id, data=data)


async def _end_move_scoring_block(host_id: int, speaker_id: int):
    data = await get_user_data(bot_object, host_id)

    speaker_role = data['players'][speaker_id]['role']
    for player_id in data['players']:  # check players, who did not clink with speaker
        if player_id != speaker_id and (player_id not in data['who_clinked_this_move_ids']) \
                and (0 < data['players'][player_id]['lives'] < 20):
            data['players'][player_id]['lives'] -= 1

    # --> speaker scoring block
    who_clicked_with_speaker_roles: list[str] = data['players'][speaker_id]['who_clinked_role']
    if not who_clicked_with_speaker_roles:  # if did not click with speaker
        data['players'][speaker_id]['lives'] -= 5

    elif len(set(who_clicked_with_speaker_roles)) == 1:  # if only opposite or same roles
        if speaker_role == who_clicked_with_speaker_roles[0]:
            data['players'][speaker_id]['lives'] -= 3
        else:
            data['players'][speaker_id]['lives'] -= 2

    elif len(set(who_clicked_with_speaker_roles)) > 1:  # if different roles clinked with speaker
        opposite_role = 'human' if speaker_role == 'wolf' else 'wolf'
        count_opposite_roles = who_clicked_with_speaker_roles.count(opposite_role)
        data['players'][speaker_id]['lives'] += 2 * count_opposite_roles

    # end move
    data['who_clinked_this_move_ids'] = []  # clear move data
    data['players'][speaker_id]['who_clinked_role'] = []  # clear speaker data
    data['current_speaker'] = 0
    data['players'][speaker_id]['is_speaker'] = False

    upd_data = await _check_append_winners(data=data)

    await update_user_data(bot_object, host_id, data=upd_data)
    return speaker_id


async def _init_next_game_circle(host_id: int):
    data = await get_user_data(bot_object, host_id)
    for player_id, player_data in data['players'].items():
        if 0 < player_data['lives'] < 20:
            data['who_did_not_speak_ids'].append(player_id)

            if player_data['is_werewolf']:  # swap role for werewolf
                role = data['players'][player_id]['role']
                data['players'][player_id]['role'] = 'human' if role == 'wolf' else 'wolf'

    shuffle(data['who_did_not_speak_ids'])
    await update_user_data(bot_object, host_id, data=data)


async def _check_append_winners(data: dict):
    for player_id, player_data in data['players'].items():
        if player_data['lives'] >= 20 and player_id not in data['winners']:
            data['winners'].append(player_id)
    return data


async def _check_continue_game(host_id: int, bot: Bot):
    data_host = await get_user_data(bot, host_id)
    active_game = data_host.get('active_game', False)
    more_one_alive = 1 <= sum(map(lambda p: p['lives'] > 0, data_host['players'].values()))
    is_three_winners = 3 >= sum(map(lambda p: p['lives'] >= 20, data_host['players'].values()))

    return active_game and more_one_alive and is_three_winners


async def _speaker_timer(speaker_id: int, time: int, bot: Bot):
    f_time = "".join([USER_TIMER[num] for num in str(time)])
    message = await bot.send_message(chat_id=speaker_id,
                                     text=f"<code>{USER_LEXICON['Toast timer message']} ⏱ {f_time}\n</code>",
                                     parse_mode='HTML')
    message_id = message.message_id
    for cur_time in range(time - 1, 0, -1):
        await asyncio.sleep(1)
        f_time = "".join([USER_TIMER[num] for num in str(cur_time)])
        await bot.edit_message_text(chat_id=speaker_id, message_id=message_id,
                                    text=f"<code>{USER_LEXICON['Toast timer message']} ⏱ {f_time}\n</code>",
                                    parse_mode='HTML')
    await bot.edit_message_text(chat_id=speaker_id, message_id=message_id,
                                text=f"<code>{USER_LEXICON['Your minute is over']}</code>")


async def clink_two_players(speaker_serial_number: int, who_clinked_id: int):
    host_id = (await get_user_data(bot_object, who_clinked_id)).get('select_host_id', 0)
    if not host_id:
        return False
    data = await get_user_data(bot_object, host_id)
    speaker_set = {value.get('user_number', 0) for value in data['players'].values()
                   if value.get('user_number', 0) == speaker_serial_number}
    if not speaker_set:
        return False
    speaker_id = speaker_set.pop()
    if who_clinked_id in data['who_clinked_this_move_ids']:
        return False

    player_who_clinked_role = data['players'][who_clinked_id]['role']
    data['players'][speaker_id]['who_clinked_role'].append(
        player_who_clinked_role)  # add role, who clinked with speaker

    if data['players'][speaker_id]['role'] == player_who_clinked_role:
        data['players'][who_clinked_id]['lives'] += 2
    else:
        data['players'][who_clinked_id]['lives'] -= 2
    data['who_clinked_this_move_ids'].append(who_clinked_id)
    await update_user_data(bot_object, host_id, data=data)


async def game_process(host_id: int, bot: Bot, speak_time: int = 60):
    if not await _check_continue_game(host_id, bot):
        return False

    speaker_id = await _get_player_who_did_not_speak_id(host_id)
    if not speaker_id:
        await _init_next_game_circle(host_id)
        speaker_id = await _get_player_who_did_not_speak_id(host_id)
        if not speaker_id:
            return False

    await _speaker_timer(speaker_id=speaker_id, time=speak_time, bot=bot)
    await _end_move_scoring_block(host_id=host_id, speaker_id=speaker_id)
    await send_info_to_users(host_id=host_id, bot=bot)
    if not await _check_continue_game(host_id, bot):
        return False

    return await game_process(host_id=host_id, bot=bot)


#
#
#
#
#

async def clear_data_game(host_id, bot: Bot):
    host_data = await get_user_data(bot, host_id)
    host_data.update({'who_did_not_speak_ids': []})  # next speakers
    host_data.update({'who_clinked_this_move_ids': []})
    host_data.update({'current_speaker': 0})
    host_data.update({'active_game': False})
    players_ids = set(host_data.get('players', {}))
    for player_id in players_ids:
        await set_user_state(bot=bot, user_id=player_id, state=None)

    await update_user_data(bot=bot, user_id=host_id, data=host_data)

# async def _make_move_for_players_test(host_id: int):
#     speaker_id = await _get_player_who_did_not_speak_id(host_id)
#     if not speaker_id:
#         return False
#
#     data = await get_data_from_user(bot_object, host_id)
#     for player_id in data['players']:  # random move with speaker, only for test
#         if player_id != speaker_id and (0 < data['players'][player_id]['lives'] < 20):  # check alive
#             if randint(0, 1):
#                 await connect_two_players(host_id, speaker_id, player_id)
#     await update_data_from_user(bot_object, host_id, data=data)
#
#     return speaker_id
