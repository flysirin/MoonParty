import asyncio

from aiogram import Bot, Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.user_states import FSMUser

from aiogram.filters import Command, CommandStart, StateFilter, Text
from filters.member_filters import CheckPassFilter, CheckSpeakerFilter, CheckUserConnectFilter
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import USER_LEXICON, USER_BUTTONS
from keyboards import user_keyboards
from services.user_services import get_active_rooms, register_user_in_room, update_user_nickname

from services import game

import logging
import re

logging.basicConfig(level=logging.INFO)
logger_user_handler = logging.getLogger(__name__)

router_user = Router()

# router_user.message.filter(CheckSpeakerFilter())
# router_user.callback_query.filter(CheckSpeakerFilter())


@router_user.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=USER_LEXICON["/start"],
                         reply_markup=user_keyboards.start_kb())
    logger_user_handler.info(f"Start for registered user, id: {message.from_user.id}")


@router_user.message(CommandStart(), StateFilter(FSMUser.success_game_enter),
                     CheckUserConnectFilter())
async def clink_with_speaker(message: Message, state: FSMContext):
    speaker_number = message.text.split()[-1]
    await game.clink_two_players(speaker_serial_number=int(speaker_number), who_clinked_id=message.from_user.id)


@router_user.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=USER_LEXICON["/help"])


@router_user.message(Text(USER_BUTTONS["Show active rooms"]), StateFilter(default_state))
async def show_active_rooms(message: Message, state: FSMContext):
    active_rooms = await get_active_rooms()
    await message.answer(
        text=f"{USER_LEXICON.get(['no active rooms', 'active rooms'][bool(active_rooms)], 'active rooms')}",
        reply_markup=user_keyboards.active_rooms_inline_kb(**active_rooms))
    await state.set_state(None)
    await asyncio.sleep(1)


@router_user.message(Text(USER_BUTTONS['Set nickname']), StateFilter(default_state))
async def set_nickname_pressed(message: Message, state: FSMContext):
    await state.set_state(FSMUser.set_nickname)
    await message.answer(text=USER_LEXICON["Input your nickname"],
                         reply_markup=user_keyboards.cancel_operation())


@router_user.message(F.text, StateFilter(FSMUser.set_nickname))
async def confirm_set_nickname(message: Message, state: FSMContext, bot: Bot):
    nickname = message.text
    # await message.answer(text=f"{USER_LEXICON['Set nickname: ']}{message.text}",
    #                      reply_markup=user_keyboards.cancel_operation())
    await state.update_data(nickname=nickname)
    await update_user_nickname(user_id=message.from_user.id, bot=bot, nickname=nickname)
    await message.answer(text=f"{USER_LEXICON['Your current nickname: ']}{nickname}")
    await state.set_state(None)
    await message.delete()


@router_user.callback_query(F.data.regexp(r"__.*__name__\d*__id__"), StateFilter(default_state))
async def get_room_for_user(callback: CallbackQuery, state: FSMContext):
    extract_data = re.search(r"__(.*)__name__(\d*)__id__", callback.data)
    try:
        room_name = extract_data.group(1)
        leader_id = extract_data.group(2)
    except BaseException as e:
        logger_user_handler.info(f"{e}")
        return await callback.message.answer(text=USER_LEXICON["Something wrong in select room"])

    await state.set_state(FSMUser.input_pass_mode)
    await state.update_data(select_room=room_name)
    await state.update_data(select_leader_id=leader_id)
    await callback.message.answer(text=f"{USER_LEXICON['Input password for room: ']}{room_name}",
                                  reply_markup=user_keyboards.cancel_operation())


@router_user.message(CheckPassFilter(), StateFilter(FSMUser.input_pass_mode))
async def success_register_in_room(message: Message, state: FSMContext):
    username: str = message.from_user.username
    nickname = (await state.get_data()).get('nickname', '')
    leader_id: int = int((await state.get_data()).get('select_leader_id', 0))
    user_id: int = message.from_user.id

    nickname = nickname if nickname else username
    cur_user_number = await register_user_in_room(username=nickname, leader_id=leader_id, user_id=user_id)

    room_name = (await state.get_data()).get('select_room', '')
    logger_user_handler.info(f"user: {username} is registered in room: {room_name}")
    await state.set_state(FSMUser.success_game_enter)
    await message.answer(text=f"{USER_LEXICON['Successful registered in room: ']}{room_name}\n"
                              f"{USER_LEXICON['Wait for the game to start']}\n"
                              f"{USER_LEXICON['Your QR code number: ']}{cur_user_number}")


@router_user.message(F.text, StateFilter(FSMUser.input_pass_mode))
async def exception_input_pass_mode(message: Message, state: FSMContext):
    await message.answer(text=USER_LEXICON["Password entry error"],
                         reply_markup=user_keyboards.cancel_operation())


#
#
#
#
#
#
#
#
#
@router_user.callback_query(Text("##cancel##operation##"), ~StateFilter(FSMUser.success_game_enter))
async def cancel_operation_room_leader(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=USER_LEXICON["Cancel operation"])
    # await state.update_data(select_room=None)
    # await state.update_data(select_leader_id=None)

    await state.set_state(None)
    await callback.message.delete()


@router_user.message(Command(commands=['cancel']))
async def cancel(message: Message, state: FSMContext):
    await message.answer(text=USER_LEXICON["All settings reset"])
    await state.set_state(None)
    await message.delete()


# @router_user.message(Command(commands=["start"]))
# async def cancel_operation_room_leader(message: Message, state: FSMContext):
#     await state.update_data(select_room=None)
#     await state.update_data(select_leader_id=None)
#     await state.set_state(None)
#     await message.delete()
