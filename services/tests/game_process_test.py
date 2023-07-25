from random import choice, shuffle, randint

data: dict = {'players': {}}


def start_init_players(count: int = 10):
    data.update({'who_did_not_speak_ids': []})  # next speakers
    data.update({'who_clinked_this_move_ids': []})
    data.update({'winners': []})
    data.update({'current_speaker': ''})
    players = data.get('players', {})

    list_roles = _init_roles(count=count)
    print(list_roles)
    for i in range(count):
        current_role = list_roles[i]
        role, is_werewolf = (current_role, False) if current_role != 'werewolf' else (choice(['wolf', 'human']), True)

        player = {i + 1: {'nickname': f"Player_{i + 1}", 'role': role, 'lives': 10,
                          'is_werewolf': is_werewolf, 'is_change_role': False,
                          'who_clinked_role': []}}
        players.update(player)
        data['who_did_not_speak_ids'].append(i + 1)
        shuffle(data['who_did_not_speak_ids'])
    data.setdefault("players", players)


def _init_roles(count: int):
    n = count
    n_werewolf, n_wolf = round(n / 5), round(2 * n / 5)
    n_human = n - n_wolf - n_werewolf
    swap_list = [n_human, n_wolf]
    shuffle(swap_list)
    n_wolf, n_human = swap_list
    list_roles = ['werewolf'] * n_werewolf + ['wolf'] * n_wolf + ['human'] * n_human
    shuffle(list_roles)
    return list_roles


def _get_player_who_did_not_speak_id():
    while data.get('who_did_not_speak_ids', []):
        speaker_id = data['who_did_not_speak_ids'].pop()
        if 0 < data['players'][speaker_id]['lives'] < 20:
            data['current_speaker'] = speaker_id
            return speaker_id
    return False


def connect_two_players(speaker_id: int, who_clinked_id: int):
    player_who_clinked_role = data['players'][who_clinked_id]['role']
    data['players'][speaker_id]['who_clinked_role'].append(
        player_who_clinked_role)  # add role, who clinked with speaker

    if data['players'][speaker_id]['role'] == player_who_clinked_role:
        data['players'][who_clinked_id]['lives'] += 2
    else:
        data['players'][who_clinked_id]['lives'] -= 2
    data['who_clinked_this_move_ids'].append(who_clinked_id)


def _make_move_for_players_test():
    speaker_id = _get_player_who_did_not_speak_id()
    if not speaker_id:
        return False

    for player_id in data['players']:  # random move with speaker, only for test
        if player_id != speaker_id and (0 < data['players'][player_id]['lives'] < 20):  # check alive
            if randint(0, 1):
                connect_two_players(speaker_id, player_id)
    return speaker_id


def _end_move_scoring_block(speaker_id: int):
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
    _check_append_winners()

    return speaker_id


def _init_next_game_circle():
    for player_id, player_data in data['players'].items():
        if 0 < player_data['lives'] < 20:
            data['who_did_not_speak_ids'].append(player_id)

            if player_data['is_werewolf']:  # swap role for werewolf
                role = data['players'][player_id]['role']
                data['players'][player_id]['role'] = 'human' if role == 'wolf' else 'wolf'

    shuffle(data['who_did_not_speak_ids'])


def _print_game_table_info(speaker_id: int):
    _data = data['players']
    print(f"=" * 52)
    print(f"{'nickname':<5} | {'role':<5} | {'lives':<5} | {'is werewolf':<5} | {'is speaker?':<5}")
    for player_id in _data:
        print(f"_" * 52)
        print(f"{_data[player_id]['nickname']:<5} | {_data[player_id]['role']:<5} |"
              f" {_data[player_id]['lives']:^5} | {['', 'werewolf'][_data[player_id]['is_werewolf']]:^11}"
              f" | {['', 'Speaker'][speaker_id == player_id]:^5}")
    print()
    print(f" " * 52)


def _check_append_winners():
    for player_id, player_data in data['players'].items():
        if player_data['lives'] >= 20 and player_id not in data['winners']:
            data['winners'].append(player_id)


def _do_game_circles(count_players: int = 5, circles: int = 10):  # test func
    start_init_players(count_players)

    for i in range(circles):
        print(f"Game circle: {i + 1}")
        print(f"+" * 52)
        while speaker_id := _make_move_for_players_test():
            _end_move_scoring_block(speaker_id=speaker_id)
            _print_game_table_info(speaker_id=speaker_id)
            # sleep(0.1)
        _init_next_game_circle()
    print(data['winners'])


#
#
#
#
#
#
#
# _do_game_circles(count_players=8, circles=10)

__data: dict = {'players': {1: {'nickname': f"Player_{1}", 'role': 'role', 'lives': 10,
                                'is_werewolf': True, 'is_change_role': False,
                                'who_clinked_role': []},
                            2: {'nickname': f"Player_{2}", 'role': 'role', 'lives': 0,
                                'is_werewolf': True, 'is_change_role': False,
                                'who_clinked_role': []},
                            }
                }


