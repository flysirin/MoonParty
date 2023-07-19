import asyncio
import logging

from aiogram import Bot, Dispatcher
from models.methods import storage
from handlers import user_handlers, admin_handlers, host_handlers
from bot_object import bot_object
from keyboards.set_menu import set_main_menu

logger_main_file = logging.getLogger(__name__)


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger_main_file.info("Starting bot")
    dp = Dispatcher(storage=storage)
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(admin_handlers.router_admin)
    dp.include_router(host_handlers.router_host)
    dp.include_router(user_handlers.router_user)

    await set_main_menu(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(bot=bot_object))
