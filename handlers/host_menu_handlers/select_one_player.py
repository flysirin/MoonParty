from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.host_states import FSMHost
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import Message, CallbackQuery
from keyboards import host_keyboards
from lexicon.lexicon import HOST_LEXICON, HOST_BUTTONS
from services import game, host_services
import logging
from handlers.host_menu_handlers.registration_menu import select_players

router_select_one_player = Router()
router_select_one_player.callback_query.filter(StateFilter(FSMHost.select_one_player))


@router_select_one_player.callback_query(Text(startswith=f"_delete_player_id_"))
async def delete_all_players(callback: CallbackQuery, state: FSMContext, bot: Bot):
    player_id = str(callback.message.text[18:-9])
    host_data = (await state.get_data())
    del host_data['players'][player_id]
    await state.update_data(data=host_data)

    await select_players(callback, state, bot)


@router_select_one_player.callback_query(Text("_exit_select_players_pressed_"))
async def exit_select_players(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await select_players(callback, state, bot)


