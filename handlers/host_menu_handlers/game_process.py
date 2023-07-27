from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.host_states import FSMHost
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import host_keyboards
from lexicon.lexicon import HOST_LEXICON, HOST_BUTTONS
from services import game, host_services
from handlers.host_menu_handlers.start_menu_handlers import init_game_process
import logging

router_game_process = Router()
router_game_process.callback_query.filter(StateFilter(FSMHost.game_process))


@router_game_process.callback_query(Text("_select_players_in_game_pressed_"))
async def select_players_in_game(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMHost.select_players_in_game)
    players = (await state.get_data()).get('players', {})
    game_info = await host_services.get_game_info(host_id=callback.from_user.id, bot=bot)
    await callback.message.edit_text(text=game_info,
                                     reply_markup=host_keyboards.select_players_in_game_inline_kb(**players))


@router_game_process.callback_query(Text("_update_host_data_pressed_"))
async def update_host_data(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        await return_game_process(callback, state, bot)
    except BaseException as e:
        return await callback.answer()


@router_game_process.callback_query(Text("_finish_game_pressed_"))
async def finish_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(text=HOST_LEXICON["Confirm finish game process"],
                                     reply_markup=host_keyboards.confirm_finish_game_process_inline_kb())


@router_game_process.callback_query(Text("_confirm_finish_game_pressed_"))
async def confirm_finish_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # await update_user_list(callback, state)
    await state.update_data(active_game=False)
    await state.update_data(active_registration=True)

    await game.clear_data_game(host_id=callback.from_user.id, bot=bot)
    await state.set_state(FSMHost.wait_register_players)
    players = (await state.get_data()).get('players', {})
    await callback.message.edit_text(text=f"{HOST_LEXICON['Waiting for players to register']} {len(players)}",
                                     reply_markup=host_keyboards.registered_players_inline_kb())


@router_game_process.callback_query(Text("_return_game_process_pressed_"))
async def return_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMHost.game_process)
    game_info = await host_services.get_game_info(host_id=callback.from_user.id, bot=bot)
    await callback.message.edit_text(text=game_info,
                                     reply_markup=host_keyboards.game_process_menu_inline_kb())
