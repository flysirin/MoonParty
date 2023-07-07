from aiogram import Bot

from models.methods import get_data_from_user
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config_data.config import ADMIN_IDS
from bot_object import bot_object

_MAIN_ADMINS: list[int] = [int(admin.strip()) for admin in ADMIN_IDS.split(',')]


class IsRoomAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        main_admin_id = _MAIN_ADMINS[0]
        data_from_admin = get_data_from_user(bot=bot_object, user_id=main_admin_id)
        usernames_admin_room = (await data_from_admin).get("room_admins", {})
        return message.from_user.username in usernames_admin_room


class IsMainAdmins(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in _MAIN_ADMINS


class IsRegisterUsers(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return False

