from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
ADMIN_IDS = env("ADMIN_IDS")


