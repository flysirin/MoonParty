# from bot_game_polling_run import storage
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import ADMIN_IDS

_MAIN_ADMINS: list[int] = [int(admin.strip()) for admin in ADMIN_IDS.split(',')]
ROOM_ADMINS: list[int] = []


class IsRoomAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ROOM_ADMINS


class IsMainAdmins(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in _MAIN_ADMINS


class IsRegisterUsers(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return False

