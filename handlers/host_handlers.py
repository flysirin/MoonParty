from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.host_states import FSMHost
from aiogram.filters import Command, CommandStart, StateFilter, Text
from filters.member_filters import IsHost
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import host_keyboards
from lexicon.lexicon import HOST_LEXICON, HOST_BUTTONS
from services import game, host_services

from handlers.host_menu_handlers.start_menu_handlers import router_start_menu
from handlers.host_menu_handlers.registration_menu import router_registration_menu
from handlers.host_menu_handlers.select_players import router_select_players
from handlers.host_menu_handlers.select_one_player import router_select_one_player
from handlers.host_menu_handlers.game_settins import router_game_settings
from handlers.host_menu_handlers.set_toast_time import router_set_toast_time
from handlers.host_menu_handlers.set_start_lives import router_set_start_lives
from handlers.host_menu_handlers.set_win_lives import router_set_win_lives
from handlers.host_menu_handlers.set_count_winners import router_set_count_winners
from handlers.host_menu_handlers.change_spread_roles import router_change_spread_roles


import logging

logging.basicConfig(level=logging.INFO)
logger_host = logging.getLogger(__name__)

router_host = Router()
router_host.message.filter(IsHost())
router_host.callback_query.filter(IsHost())

router_host.include_router(router_start_menu)
router_host.include_router(router_registration_menu)
router_host.include_router(router_select_players)
router_host.include_router(router_select_one_player)
router_host.include_router(router_game_settings)
router_host.include_router(router_set_toast_time)
router_host.include_router(router_set_start_lives)
router_host.include_router(router_set_win_lives)
router_host.include_router(router_set_count_winners)
router_host.include_router(router_change_spread_roles)


@router_host.callback_query(Text("_finish_game_pressed_"), StateFilter(FSMHost.game_process))
async def start_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # await update_user_list(callback, state)
    # await state.update_data(active_registration=False)
    await state.update_data(active_game=False)

    await game.clear_data_game(host_id=callback.from_user.id, bot=bot)

    await state.set_state(FSMHost.wait_register_players)


@router_host.message(Command(commands=["cancel"]))
async def command_cancel(message: Message, state: FSMContext, bot: Bot):
    # await message.delete()
    # await bot.delete_my_commands()
    await message.answer(text=HOST_LEXICON["States canceled"], reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)


@router_host.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=HOST_LEXICON["/help"])

# @router_host.callback_query()
# async def test_callback(callback: CallbackQuery):
#     await callback.answer(text=f"from router_host callback data: {callback.data}")
