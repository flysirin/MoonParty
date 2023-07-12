from time import sleep
from random import choice, shuffle
from pprint import pprint

data: dict = {'players': {}}

user_id = 0
username = ''
player_template: dict = {user_id: {'nickname': username, 'role': None, 'lives': 10, 'is_speaker': False,
                                   'is_werewolf': False, 'did_he_say': False, 'is_change_role': False,
                                   'who_checked_role': []}}


def start_init_players(count: int = 10):
    data.update({'who_did_not_speak': []})
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
        data['who_did_not_speak'].append(i + 1)
        shuffle(data['who_did_not_speak'])
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
    if not data.get('who_did_not_speak', []):
        return False
    return data['who_did_not_speak'].pop()


start_init_players(5)

# pprint(data)
for i in range(5):
    sleep(1)
    _id = get_player_who_did_not_speak_id()
    print(_id)

print(data)
