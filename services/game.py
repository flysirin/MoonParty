from random import choice, shuffle, randint
from bot_object import bot_object
from models.methods import get_data_from_user, update_data_from_user


async def start_init_players(leader_id: int):
    data = await get_data_from_user(bot_object, leader_id)
    data.update({'who_did_not_speak_ids': []})  # next speakers
    data.update({'who_clinked_this_move_ids': []})
    data.update({'winners': []})
    data.update({'current_speaker': ''})
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
    await update_data_from_user(bot_object, leader_id, data=data)


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


async def _get_player_who_did_not_speak_id(leader_id: int):
    data = await get_data_from_user(bot_object, leader_id)
    while data.get('who_did_not_speak_ids', []):
        speaker_id = data['who_did_not_speak_ids'].pop()
        if 0 < data['players'][speaker_id]['lives'] < 20:
            data['current_speaker'] = speaker_id
            await update_data_from_user(bot_object, leader_id, data=data)
            return speaker_id
    return False


async def connect_two_players(leader_id: int, speaker_id: int, who_clinked_id: int):
    data = await get_data_from_user(bot_object, leader_id)

    player_who_clinked_role = data['players'][who_clinked_id]['role']
    data['players'][speaker_id]['who_clinked_role'].append(
        player_who_clinked_role)  # add role, who clinked with speaker

    if data['players'][speaker_id]['role'] == player_who_clinked_role:
        data['players'][who_clinked_id]['lives'] += 2
    else:
        data['players'][who_clinked_id]['lives'] -= 2
    data['who_clinked_this_move_ids'].append(who_clinked_id)
    await update_data_from_user(bot_object, leader_id, data=data)


async def _end_move_scoring_block(leader_id: int, speaker_id: int):
    data = await get_data_from_user(bot_object, leader_id)

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
    data['current_speaker'] = ''

    upd_data = await _check_append_winners(data=data)

    await update_data_from_user(bot_object, leader_id, data=upd_data)
    return speaker_id


async def _init_next_game_circle(leader_id: int):
    data = await get_data_from_user(bot_object, leader_id)
    for player_id, player_data in data['players'].items():
        if 0 < player_data['lives'] < 20:
            data['who_did_not_speak_ids'].append(player_id)

            if player_data['is_werewolf']:  # swap role for werewolf
                role = data['players'][player_id]['role']
                data['players'][player_id]['role'] = 'human' if role == 'wolf' else 'wolf'

    shuffle(data['who_did_not_speak_ids'])
    await update_data_from_user(bot_object, leader_id, data=data)


async def _check_append_winners(data: dict):
    for player_id, player_data in data['players'].items():
        if player_data['lives'] >= 20 and player_id not in data['winners']:
            data['winners'].append(player_id)
    return data


async def start_move(leader_id: int):
    speaker_id = await _get_player_who_did_not_speak_id(leader_id)
    if not speaker_id:
        await _init_next_game_circle(leader_id)
        return False

    return speaker_id

#
#
#
#
#
async def _make_move_for_players_test(leader_id: int):
    speaker_id = await _get_player_who_did_not_speak_id(leader_id)
    if not speaker_id:
        return False

    data = await get_data_from_user(bot_object, leader_id)
    for player_id in data['players']:  # random move with speaker, only for test
        if player_id != speaker_id and (0 < data['players'][player_id]['lives'] < 20):  # check alive
            if randint(0, 1):
                await connect_two_players(leader_id, speaker_id, player_id)
    await update_data_from_user(bot_object, leader_id, data=data)

    return speaker_id
