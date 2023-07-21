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

router_wait_registration = Router()
router_wait_registration.callback_query.filter(StateFilter(FSMHost.wait_register_players))


@router_wait_registration.callback_query(Text("_update_user_lists_"))
async def update_user_list(callback: CallbackQuery, state: FSMContext):
    players = (await state.get_data()).get('players', {})
    try:
        await callback.message.edit_text(text=f"{HOST_LEXICON['Waiting for players to register']} {len(players)}",
                                         reply_markup=callback.message.reply_markup)
    except BaseException as e:
        logging.getLogger(__name__).error(f"{e}")
    await callback.answer()


@router_wait_registration.callback_query(Text("_start_game_pressed_"))
async def start_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    players = (await state.get_data()).get('players', {})
    if not len(players) >= 1:
        return await callback.answer(text=HOST_LEXICON["Unable to start"], show_alert=True)
    await state.set_state(FSMHost.game_process)
    await state.update_data(active_registration=False)
    await state.update_data(active_game=True)
    await game.clear_data_game(host_id=callback.from_user.id, bot=bot)

    await game.game_process(host_id=callback.from_user.id, bot=bot)
    game_info = await host_services.get_game_info(host_id=callback.from_user.id, bot=bot)
    await callback.message.edit_text(text=game_info,
                                     reply_markup=host_keyboards.game_process_menu())
    await game.start_init_players(host_id=callback.from_user.id)


@router_wait_registration.callback_query(Text("_view_qr_code_pressed_"))
async def view_qr_code(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await host_services.send_curr_qr_code(chat_id=callback.from_user.id,
                                          host_username=callback.from_user.username,
                                          state=state, bot=bot)
    players = (await state.get_data()).get('players', {})
    await callback.message.answer(text=f"{HOST_LEXICON['Waiting for players to register']} {len(players)}",
                                  reply_markup=host_keyboards.registered_players_inline_kb())
    await state.set_state(FSMHost.wait_register_players)
    await state.update_data(active_registration=True)
    await callback.message.delete()


@router_wait_registration.callback_query(Text("_select_players_pressed_"))
async def select_players(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMHost.select_players)
    players = (await state.get_data()).get('players', {})
    await callback.message.edit_text(text=HOST_LEXICON["Choose a player"],
                                     reply_markup=host_keyboards.select_player_inline_kb(**players))


@router_wait_registration.callback_query(Text("_setting_game_pressed_"))
async def settings_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    pass


@router_wait_registration.callback_query(Text("_exit_main_menu_pressed_"))
async def update_user_list(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.message.edit_text(text=HOST_LEXICON["Choose an option"],
                                     reply_markup=host_keyboards.main_menu_inline_kb())
    await state.update_data(active_registration=False)
    await callback.answer()


@router_wait_registration.callback_query(Text("__hide__qr_code__"))
async def hide_qr_code(callback: CallbackQuery):
    await callback.message.delete()
