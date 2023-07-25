from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.host_states import FSMHost
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import host_keyboards
from lexicon.lexicon import HOST_LEXICON, HOST_BUTTONS
from services import game, host_services
import logging

router_select_players = Router()
router_select_players.callback_query.filter(StateFilter(FSMHost.select_players))


@router_select_players.callback_query(Text("_exit_reg_menu_pressed_"))
async def exit_registration_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMHost.wait_register_players)
    players = (await state.get_data()).get('players', {})
    await callback.message.edit_text(text=f"{HOST_LEXICON['Waiting for players to register']} {len(players)}",
                                     reply_markup=host_keyboards.registered_players_inline_kb())
    await state.update_data(active_registration=True)


@router_select_players.callback_query(Text("_delete_all_players_pressed_"))
async def delete_all(callback: CallbackQuery, state: FSMContext):
    await state.update_data(data={'players': {}})
    await exit_registration_menu(callback, state)


@router_select_players.callback_query(Text(contains="__player__user_id__"))
async def select_player(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMHost.select_one_player)
    player_id: int = int(callback.message.text[2:-19])
    players = (await state.get_data()).get('players', {})
    nickname = players[int(player_id)]['nickname']
    await callback.message.edit_text(text=f"{HOST_LEXICON['chose option for player']} {nickname}",
                                     reply_markup=host_keyboards.select_one_player_inline_kb(player=player_id))


