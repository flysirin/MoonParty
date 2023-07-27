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
from handlers.host_menu_handlers.game_process import select_players_in_game

router_select_one_player_in_game = Router()
router_select_one_player_in_game.callback_query.filter(StateFilter(FSMHost.select_one_player_in_game))


@router_select_one_player_in_game.callback_query(Text(startswith=["_down_lives_player_id_", '_up___lives_player_id_']))
async def delete_all_players(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    player_id: str = callback.data[22:-9]
    nickname = host_data['players'][player_id]['nickname']

    if callback.data.startswith("_up___lives_player_id_pressed_"):
        host_data['players'][player_id]['lives'] += 1

    elif callback.data.startswith("_down_lives_player_id_pressed_"):
        if host_data['players'][player_id]['lives'] <= 0:
            return await callback.answer()
        host_data['players'][player_id]['lives'] -= 1

    lives = host_data['players'][player_id]['lives']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Player:']} {nickname}\n"
                                          f"{HOST_LEXICON['lives:']} {lives}",
                                     reply_markup=host_keyboards.select_one_player_in_game_inline_kb(
                                         player_id=player_id))


@router_select_one_player_in_game.callback_query(Text("_exit_select_players_pressed_"))
async def return_select_players(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await select_players_in_game(callback, state, bot)
