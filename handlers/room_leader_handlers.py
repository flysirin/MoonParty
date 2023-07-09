from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.room_leader_states import FSMRoomLeader

from aiogram.filters import Command, CommandStart, StateFilter, Text, ChatMemberUpdatedFilter
from filters.member_filters import IsRoomLeader

from aiogram.types import Message, CallbackQuery
from keyboards import room_leader_keyboards

from lexicon.lexicon import LEXICON
from models.methods import set_data_from_user, get_data_from_user
import logging

logging.basicConfig(level=logging.INFO)
logger_leader_handler = logging.getLogger(__name__)

router_room_leader = Router()
router_room_leader.message.filter(IsRoomLeader())


@router_room_leader.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                              f"Password:{(await state.get_data()).get('password', '')}",
                         reply_markup=room_leader_keyboards.room_leader_inline_kb())
    await state.set_state(None)


@router_room_leader.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["/help_admin"])


@router_room_leader.callback_query(Text("change_room_name_pressed"))
async def create_room(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMRoomLeader.input_room_name)
    await callback.answer(text="Input room name")


@router_room_leader.message(F.text, StateFilter(FSMRoomLeader.input_room_name))
async def input_room_name(message: Message, state: FSMContext):
    await state.update_data(room_name=message.text)
    await state.set_state(FSMRoomLeader.input_password)
    await state.set_state(None)


@router_room_leader.callback_query(Text("change_pass_pressed"))
async def input_password(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                                          f"Password: {(await state.get_data()).get('password')}",
                                     reply_markup=callback.message.reply_markup)
    await state.set_state(FSMRoomLeader.input_password)
    await callback.answer(text="Input Password")


@router_room_leader.callback_query(Text("start_game_pressed"))
async def start_game(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not (data.get('room_name', '') and data.get('password', '')):
        await callback.answer(text="Can't start without Room Name or pass")
    await callback.answer(text="Game start successfully")
# interface


@router_room_leader.callback_query(Text("cancel_data"))
async def cancel_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                                          f"Password:{(await state.get_data()).get('password', '')}",
                                     reply_markup=callback.message.reply_markup)
    await callback.answer(text="All data canceled")


@router_room_leader.message(Command("cancel"))
async def command_cancel(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(None)


@router_room_leader.callback_query(Text("cancel_state"))
async def cancel_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.answer(text="States canceled")


@router_room_leader.message(Text("Get data storage"))
async def get_data_storage(message: Message, state: FSMContext):
    await message.answer(text=f"{state.get_data()}")