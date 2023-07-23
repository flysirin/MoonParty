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

router_game_settings = Router()
router_game_settings.callback_query.filter(StateFilter(FSMHost.game_settings))


@router_game_settings.callback_query(Text("_toast_time_pressed"))
async def change_toast_time(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMHost.set_toast_time)
    toast_time = (await state.get_data()).get('settings', {}).get('toast_time', 60)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Toast time:']} {toast_time}",
                                     reply_markup=host_keyboards.set_toast_time_inline_kb())


@router_game_settings.callback_query(Text("_change_start_lives_pressed"))
async def change_start_lives(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMHost.set_start_lives)
    start_lives = (await state.get_data()).get('settings', {}).get('start_lives', 10)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Start lives:']} {start_lives}",
                                     reply_markup=host_keyboards.set_lives_inline_kb())


@router_game_settings.callback_query(Text("_change_win_lives_pressed"))
async def change_win_lives(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMHost.set_win_lives)
    win_lives = (await state.get_data()).get('settings', {}).get('win_lives', 20)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Win lives:']} {win_lives}",
                                     reply_markup=host_keyboards.set_lives_inline_kb())


@router_game_settings.callback_query(Text("_update_qr_code_data_pressed_"))
async def update_qr_code_data(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await host_services.update_qr_code_data(state)
    await callback.answer(text=HOST_LEXICON["Update entrance data"], show_alert=True)


@router_game_settings.callback_query(Text("_reset_settings_pressed_"))
async def reset_default_settings(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await host_services.reset_game_settings(state)
    await callback.answer(text=HOST_LEXICON["Reset game settings"], show_alert=True)


@router_game_settings.callback_query(Text("_exit_main_menu_pressed_"))
async def exit_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(text=HOST_LEXICON["Choose an option"],
                                     reply_markup=host_keyboards.main_menu_inline_kb())
    await state.set_state(None)
