from aiogram import Bot, Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.user_states import FSMUser

from aiogram.filters import Command, CommandStart, StateFilter, Text
from filters.member_filters import IsRegisterUsers

from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON

import logging

logging.basicConfig(level=logging.INFO)
logger_user_handler = logging.getLogger(__name__)

router_user = Router()
router_user.message.filter(IsRegisterUsers())


@router_user.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    logger_user_handler.info(f"Start for registered user, id: {message.from_user.id}")
    await message.answer(text=LEXICON["/start"])


@router_user.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["/help"])

# @router.message(CommandStart(), StateFilter(FSMUser.in_game))
# async def process_
