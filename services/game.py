from player import Player

from random import choice, shuffle


class Game:
    def __init__(self, count_players=0, room_id=None):
        self.count_players = count_players
        self.roles = []
        self._init_roles()
        self.players = {}
        self.init_players()

    def game_turn(self):
        pass

    def _init_roles(self):
        n = self.count_players
        n_werewolf, n_wolf = round(n / 5), round(2 * n / 5)
        n_human = n - n_wolf - n_werewolf
        swap_list = [n_human, n_wolf]
        shuffle(swap_list)
        n_wolf, n_human = swap_list
        list_roles = ['werewolf'] * n_werewolf + ['wolf'] * n_wolf + ['human'] * n_human

        shuffle(list_roles)
        self.roles = list_roles
        return list_roles

    def get_roles(self):
        return self.roles

    def init_players(self):
        self.players = {i: Player(in_game=True, role=self.roles[i]) for i in range(self.count_players)}




game = Game(10)
_list_roles = game.get_roles()
print(_list_roles)
print(game.players)
# print(f"count_wolfs: {_list_roles.count('wolf')}")
# print(f"count_humans: {_list_roles.count('human')}")
# print(f"count_werewolf's: {_list_roles.count('werewolf')}")
