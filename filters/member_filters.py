from aiogram import Bot
from models.methods import get_data_from_user, update_data_from_user
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import ADMIN_IDS
from bot_object import bot_object
from services.user_services import get_user_id_by_serial_number

_MAIN_ADMINS: list[int] = [int(admin.strip()) for admin in ADMIN_IDS.split(',')]


class IsRoomLeader(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        main_admin_id = _MAIN_ADMINS[0]
        data_from_admin = await get_data_from_user(bot=bot_object, user_id=main_admin_id)
        room_leaders = data_from_admin.get("room_leaders", {})
        username = message.from_user.username
        user_leader_id: int = message.from_user.id

        if username in room_leaders:
            if not room_leaders.get(username, {}):
                room_leaders.update({username: {'user_id': user_leader_id}})
                data_from_admin.update(room_leaders)
                await update_data_from_user(bot=bot_object, user_id=main_admin_id, data=data_from_admin)
            return True
        return False


class IsMainAdmins(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in _MAIN_ADMINS


class CheckPassFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_data = await get_data_from_user(bot=bot_object, user_id=message.from_user.id)
        select_leader_id = user_data.get("select_leader_id", 0)
        leader_data = await get_data_from_user(bot=bot_object, user_id=int(select_leader_id))
        leader_pass = leader_data.get("password", "")
        return leader_pass == message.text


class CheckSpeakerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        leader_id = (await get_data_from_user(bot_object, user_id)).get('select_leader_id', 0)
        speaker_id = (await get_data_from_user(bot_object, leader_id)).get('current_speaker', '')

        return speaker_id != user_id


class CheckUserConnectFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        serial_user_num = message.text.split()[-1]
        if not serial_user_num.isdigit():
            return False

        leader_id = (await get_data_from_user(bot_object, user_id=user_id)).get('select_leader_id', 0)
        if leader_id:
            players = (await get_data_from_user(bot_object, user_id=leader_id)).get('players', {})
            is_active_game = players.get('active_game', False)
            is_alive_not_winner = 0 < players[user_id]['lives'] < 20
            not_speaker = players.get('current_speaker', '') != user_id
            correct_number = int(serial_user_num) in {number.get('user_number', '') for number in players.values()}

            return is_alive_not_winner and not_speaker and is_active_game and correct_number




