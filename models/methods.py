from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.fsm.storage.base import StorageKey, StateType
from aiogram import Bot
from bot_object import bot_object

# Initialize  Redis storage
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


async def get_user_data(bot: Bot, user_id: int) -> dict[int | str]:
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    data_from_user = await storage.get_data(bot=bot, key=storage_key)
    return data_from_user


async def set_user_data(bot: Bot, user_id: int, data: dict) -> None:
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    await storage.set_data(bot=bot, key=storage_key, data=data)


async def update_user_data(bot: Bot, user_id: int, data: dict) -> None:
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    await storage.update_data(bot=bot, key=storage_key, data=data)


async def set_user_state(bot: Bot, user_id: int, state: StateType = None):
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    await storage.set_state(bot=bot, key=storage_key, state=state)


async def get_user_state(bot: Bot, user_id: int):
    storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
    await storage.get_state(bot=bot, key=storage_key)
