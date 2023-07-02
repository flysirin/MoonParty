from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.fsm.storage.base import StorageKey
from aiogram import Bot

# Initialize  Redis storage
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


async def get_data_from_user(bot: Bot, user_id: int) -> dict[int | str]:
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    data_from_user = await storage.get_data(bot=bot, key=storage_key)
    return data_from_user


async def set_data_from_user(bot: Bot, user_id: int, data: dict) -> None:
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    await storage.set_data(bot=bot, key=storage_key, data=data)


async def update_data_from_user(bot: Bot, user_id: int, data: dict) -> None:
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    await storage.update_data(bot=bot, key=storage_key, data=data)

