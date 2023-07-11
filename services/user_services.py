from bot_object import bot_object
from models.methods import get_data_from_user, update_data_from_user, set_data_from_user
from config_data.config import ADMIN_IDS


async def get_active_rooms():
    main_admin_id = int(ADMIN_IDS.split(',')[0])
    data = await get_data_from_user(bot=bot_object, user_id=main_admin_id)
    room_leaders = data.get('room_leaders', {})

    active_leaders = dict()
    for nickname, user_data in room_leaders.items():
        if user_data.get('user_id', {}):
            active_leaders.update({nickname: user_data.get('user_id')})

    active_rooms = dict()
    for nickname, user_id in active_leaders.items():
        data_form_leader = await get_data_from_user(bot=bot_object, user_id=user_id)
        room_name = data_form_leader.get('room_name', None)
        if data_form_leader.get('is_active', False):
            active_rooms.update({room_name: user_id})
    return active_rooms
