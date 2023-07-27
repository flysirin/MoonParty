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

router_select_players_in_game = Router()
router_select_players_in_game.callback_query.filter(StateFilter(FSMHost.select_players_in_game))


@router_select_players_in_game.callback_query(Text(contains="__player__user_id__"))
async def select_player(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMHost.select_one_player_in_game)
    player_id: str = callback.data[2:-19]
    players = (await state.get_data()).get('players', {})
    nickname = players[player_id]['nickname']
    lives = players[player_id]['lives']
    await callback.message.edit_text(text=f"{HOST_LEXICON['Player:']} {nickname}\n"
                                          f"{HOST_LEXICON['lives:']} {lives}",
                                     reply_markup=host_keyboards.select_one_player_in_game_inline_kb(player_id=player_id))


@router_select_players_in_game.callback_query(Text("_return_game_process_pressed_"))
async def return_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    game_info = await host_services.get_game_info(host_id=callback.from_user.id, bot=bot)
    await state.set_state(FSMHost.game_process)
    try:
        await callback.message.edit_text(text=game_info,
                                         reply_markup=host_keyboards.game_process_menu_inline_kb())
    except BaseException as e:
        return await callback.answer()
