import asyncio
import logging

from aiogram import Bot, Dispatcher

from models.methods import storage

from handlers import user_handlers, admin_handlers
from config_data.config import BOT_TOKEN, ADMIN_IDS

logging.basicConfig(level=logging.WARNING)
logger_main_file = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Create database of users
user_dict: dict[int, dict[str, str | int | bool]] = {}

# bot.delete_webhook(drop_pending_updates=True)

# Register routers in Dispatcher
dp.include_router(admin_handlers.router_admin)
dp.include_router(user_handlers.router_user)


if __name__ == '__main__':
    dp.run_polling(bot)
