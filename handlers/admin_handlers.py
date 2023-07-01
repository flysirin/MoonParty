from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.admin_states import FSMAdmin

from aiogram.filters import Command, CommandStart, StateFilter, Text, ChatMemberUpdatedFilter
from filters.member_filters import IsRoomAdmin, IsMainAdmins

from aiogram.types import Message, CallbackQuery
from keyboards import keyboards

from lexicon.lexicon import LEXICON
from models.methods import redis, storage
import logging
import json

logging.basicConfig(level=logging.INFO)
logger_admin_handler = logging.getLogger(__name__)

router_admin = Router()
router_admin.message.filter(IsMainAdmins())


@router_admin.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    logger_admin_handler.info(f"Command start for main admins, id: {message.from_user.id}")
    await message.answer(text=LEXICON["/start_admin"],
                         reply_markup=keyboards.create_admin_room_kb())


@router_admin.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["/help_admin"])


@router_admin.message(Text(text="Get data storage"), StateFilter(default_state))
async def get_data_storage(message: Message, state: FSMContext):
    data_bytes = await redis.get(name="my_data")
    dict_data = json.loads(data_bytes)
    await message.answer(text=f"{dict_data}")


@router_admin.message(Text(text="Set data storage"), StateFilter(default_state))
async def set_data_storage(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.set_user)
    await message.answer(text="Input User ID")


@router_admin.message(StateFilter(FSMAdmin.set_user))
async def input_user_id(message: Message, state: FSMContext):
    if message.text:
        json_obj = {"user_id": 4242424242}
        json_string = json.dumps(json_obj)
        await redis.set(name="my_data", value=json_string)
    await state.clear()
    await message.answer(text="Data updated")




