from aiogram import Bot, Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.admin_states import FSMAdmin

from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters import Command, CommandStart, Text

from aiogram.types import Message, CallbackQuery
from keyboards import keyboards

from lexicon.lexicon import LEXICON

import logging

logging.basicConfig(level=logging.WARNING)
logger_user_handler = logging.getLogger(__name__)

router = Router()
# router.message.filter(AdminRoomFilter())


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON["/start"],
                         reply_markup=keyboards.create_admin_room_kb())


@router.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["/help"])










