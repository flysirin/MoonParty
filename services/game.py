from player import Player

from random import choice, shuffle


class Game:
    def __init__(self, room_id: int = None, user_ids: set[int] = None, lives: int = 10):
        self.__user_ids = user_ids
        self.__count_players = len(user_ids)
        self.__lives = lives
        self.__roles = []
        self._init_roles()
        self.__players = []
        self.init_players()

    def _init_roles(self):
        n = self.__count_players
        n_werewolf, n_wolf = round(n / 5), round(2 * n / 5)
        n_human = n - n_wolf - n_werewolf
        swap_list = [n_human, n_wolf]
        shuffle(swap_list)
        n_wolf, n_human = swap_list
        list_roles = ['werewolf'] * n_werewolf + ['wolf'] * n_wolf + ['human'] * n_human

        shuffle(list_roles)
        self.__roles = list_roles
        return list_roles

    @property
    def get_roles(self) -> list[str]:
        return self.__roles

    @property
    def get_players(self) -> list[Player]:
        return self.__players

    def init_players(self) -> None:
        for i, user_id in enumerate(self.__user_ids):
            self.__players.append(Player(user_id=user_id,
                                         lives=self.__lives,
                                         in_game=True,
                                         role=self.get_roles[i]))

    def get_player_by_id(self, user_id: int = None) -> Player | bool:
        for player in self.get_players:
            if user_id == player.user_id:
                return player
        return False

    def game_turn(self):
        pass


set_user_ids = {i for i in range(10)}

game = Game(user_ids=set_user_ids)
print(game.get_roles, "\n")
for player in game.get_players:
    print(f"player_id: {player.user_id},"
          f" lives: {player.lives},"
          f" is_alive: {player.is_alive},"
          F" in_game: {player.in_game}"
          f" role: {player.role}")

# print(f"count_wolfs: {_list_roles.count('wolf')}")
# print(f"count_humans: {_list_roles.count('human')}")
# print(f"count_werewolf's: {_list_roles.count('werewolf')}")
