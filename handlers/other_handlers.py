from aiogram import Router, F

from aiogram.filters import Command, CommandStart, Text

from aiogram.types import Message
# from lexicon.lexicon import LEXICON

import logging

logging.basicConfig(level=logging.INFO)
logger_user_handler = logging.getLogger(__name__)

router_user_no_register = Router()


# @router_user_no_register.message(CommandStart())
# async def process_start_command(message: Message):
#     logger_user_handler.info(f"Start for no register user, id: {message.from_user.id}")
#     await message.answer(text=LEXICON["/start"])
#
#
# @router_user_no_register.message(Command(commands=["help"]))
# async def process_help_command(message: Message):
#     await message.answer(text=LEXICON["/help"])
