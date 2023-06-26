from aiogram import Bot, Dispatcher, types, F

from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import (CallbackQuery, InlineKeyboardButton, 
                           InlineKeyboardMarkup, Message, PhotoSize)

from handlers import user_handlers
from config_data.config import BOT_TOKEN, ADMIN_IDS


# Inicialize  MemoryStorage
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=storage)

# Create data base of users
user_dict: dict[int, dict[str, str | int | bool]] = {}


bot.delete_webhook(drop_pending_updates=True)

# Register routers in Dispatcher
dp.include_router(user_handlers.router)

# Create class heritable from StateGroup for states our FSM
class FSMFillForm(StatesGroup):
    # Create instances of the State class, sequentially
    # listing the possible states it will be in
    # bot at different moments of interaction with the user
    
    fill_name = State() # State waiting for name input
    fill_age = State() # State waiting for age input
    fill_gender = State() # Gender pending state
    upload_photo = State() # State of pending photo upload
    fill_education = State() # State of waiting for education selection
    fill_wish_news = State() # Wait state to select whether to receive news

if __name__ =='__main__':
    dp.run_polling(bot)











































