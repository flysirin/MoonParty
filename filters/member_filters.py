from aiogram import Bot
from models.methods import get_user_data, update_user_data
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import ADMIN_IDS
from bot_object import bot_object

_MAIN_ADMINS: list[int] = [int(admin.strip()) for admin in ADMIN_IDS.split(',')]


class IsHost(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        main_admin_id = _MAIN_ADMINS[0]
        data_from_admin = await get_user_data(bot=bot_object, user_id=main_admin_id)
        room_hosts = data_from_admin.get("hosts", {})
        username = message.from_user.username
        user_host_id: int = message.from_user.id

        if username in room_hosts:
            if not room_hosts.get(username, {}):
                room_hosts.update({username: {'user_id': user_host_id}})
                data_from_admin.update(room_hosts)
                await update_user_data(bot=bot_object, user_id=main_admin_id, data=data_from_admin)
            return True
        return False


class IsMainAdmins(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in _MAIN_ADMINS


class CheckPassFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_data = await get_user_data(bot=bot_object, user_id=message.from_user.id)
        select_host_id = user_data.get("select_host_id", 0)
        host_data = await get_user_data(bot=bot_object, user_id=int(select_host_id))
        host_pass = host_data.get("password", "")
        return host_pass == message.text


class CheckSpeakerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        host_id = (await get_user_data(bot_object, user_id)).get('select_host_id', 0)
        speaker_id = (await get_user_data(bot_object, host_id)).get('current_speaker', '')

        return speaker_id != user_id


class CheckUserConnectFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        serial_user_num = message.text.split()[-1]
        if not serial_user_num.isdigit():
            return False

        host_id = (await get_user_data(bot_object, user_id=user_id)).get('select_host_id', 0)
        if host_id:
            players = (await get_user_data(bot_object, user_id=host_id)).get('players', {})
            is_active_game = players.get('active_game', False)
            is_alive_not_winner = 0 < players[user_id]['lives'] < 20
            not_speaker = players.get('current_speaker', '') != user_id
            correct_number = int(serial_user_num) in {number.get('user_number', '') for number in players.values()}

            return is_alive_not_winner and not_speaker and is_active_game and correct_number




