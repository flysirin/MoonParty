import asyncio

from aiogram import Bot, Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.user_states import FSMUser

from aiogram.filters import Command, CommandStart, StateFilter, Text
from filters.member_filters import IsRegisterUsers
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON
from keyboards import user_keyboards
from services.other import get_active_rooms

import logging

logging.basicConfig(level=logging.INFO)
logger_user_handler = logging.getLogger(__name__)

router_user = Router()
router_user.message.filter(IsRegisterUsers())


@router_user.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    logger_user_handler.info(f"Start for registered user, id: {message.from_user.id}")
    await message.answer(text=LEXICON["/start"],
                         reply_markup=user_keyboards.start_kb())


@router_user.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["/help"])


@router_user.message(Text("Show active rooms"))
async def show_active_rooms(message: Message, state: FSMContext):
    active_rooms = await get_active_rooms()
    await message.answer(text=f"Active rooms. Press for enter.",
                         reply_markup=user_keyboards.active_rooms(**active_rooms))
    await asyncio.sleep(1)
