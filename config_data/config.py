from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
ADMIN_IDS = env("ADMIN_IDS")

host_game_data: dict = {
    'settings':
        {
            'toast_time': 60,
            'percent_role': {'human': 40, 'wolf': 40, 'werewolf': 20},
            'start_lives': 10,
            'win_lives': 20,
            'count_winners': 1,
        }
}
