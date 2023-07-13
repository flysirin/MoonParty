from time import sleep
from random import choice, shuffle, randint
from pprint import pprint

data: dict = {'players': {}}

user_id = 0
username = ''
player_template: dict = {user_id: {'nickname': username, 'role': None, 'lives': 10, 'is_speaker': False,
                                   'is_werewolf': False, 'did_he_say': False, 'is_change_role': False,
                                   'who_checked_role': []}}


def start_init_players(count: int = 10):
    data.update({'who_did_not_speak_ids': []})  # next speakers
    data.update({'who_checked_this_move_ids': []})
    players = data.get('players', {})

    list_roles = init_roles(count=count)
    print(list_roles)
    for i in range(count):
        current_role = list_roles[i]
        role, is_werewolf = (current_role, False) if current_role != 'werewolf' else (choice(['wolf', 'human']), True)

        player = {i + 1: {'nickname': f"Player_{i + 1}", 'role': role, 'lives': 10, 'is_speaker': False,
                          'is_werewolf': is_werewolf, 'did_he_say': False, 'is_change_role': False,
                          'who_checked_role': []}}
        players.update(player)
        data['who_did_not_speak_ids'].append(i + 1)
        shuffle(data['who_did_not_speak_ids'])
    data.setdefault("players", players)


def init_roles(count: int):
    n = count
    n_werewolf, n_wolf = round(n / 5), round(2 * n / 5)
    n_human = n - n_wolf - n_werewolf
    swap_list = [n_human, n_wolf]
    shuffle(swap_list)
    n_wolf, n_human = swap_list
    list_roles = ['werewolf'] * n_werewolf + ['wolf'] * n_wolf + ['human'] * n_human
    shuffle(list_roles)
    return list_roles


def get_player_who_did_not_speak_id():
    if not data.get('who_did_not_speak_ids', []):
        return False
    return data['who_did_not_speak_ids'].pop()


def connect_two_players(speaker_id: int, who_checked_id: int):
    player_who_checked_role = data['players'][who_checked_id]['role']
    data['players'][speaker_id]['who_checked_role'].append(player_who_checked_role)  # add role, who checked with speaker
    if data['players'][speaker_id]['role'] == player_who_checked_role:
        data['players'][who_checked_id]['lives'] += 2
    else:
        data['players'][who_checked_id]['lives'] -= 2
    data['who_checked_this_move_ids'].append(who_checked_id)


def make_move_for_players():
    speaker_id = get_player_who_did_not_speak_id()
    if not speaker_id:
        return False

    speaker_role = data['players'][speaker_id]['role']
    for player_id in data['players']:                           # random move with speaker, only for test
        if player_id != speaker_id:
            if randint(0, 1):
                connect_two_players(speaker_id, player_id)

    for player_id in data['players']:                           # check players, who did not check with speaker
        if player_id != speaker_id and (player_id not in data['who_checked_this_move_ids']):
            data['players'][player_id]['lives'] -= 1

    # --> speaker scoring block
    who_checked_with_speaker_roles: list[str] = data['players'][speaker_id]['who_checked_role']
    if not who_checked_with_speaker_roles:                        # if did not check with speaker
        data['players'][speaker_id]['lives'] -= 5

    elif len(set(who_checked_with_speaker_roles)) == 1:           # if only opposite or same roles
        if speaker_role == who_checked_with_speaker_roles[0]:
            data['players'][speaker_id]['lives'] -= 3
        else:
            data['players'][speaker_id]['lives'] -= 2

    elif len(set(who_checked_with_speaker_roles)) != 1:           # if different roles checked with speaker
        opposite_role = 'human' if speaker_role == 'wolf' else 'human'
        count_opposite_roles = who_checked_with_speaker_roles.count(opposite_role)
        data['players'][speaker_id]['lives'] += 2 * count_opposite_roles

    # end move
    data['who_checked_this_move_ids'] = []  # clear move data

    return True


#
#
#
#
#
#
#
# start init players
start_init_players(5)
# pprint(data)
for i in range(10):
    make_move_for_players()
pprint(data)










