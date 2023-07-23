from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.host_states import FSMHost
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import host_keyboards
from lexicon.lexicon import HOST_LEXICON, HOST_BUTTONS
from services import game, host_services
from handlers.host_menu_handlers.start_menu_handlers import game_settings
import logging

router_set_toast_time = Router()
router_set_toast_time.callback_query.filter(StateFilter(FSMHost.set_toast_time))


@router_set_toast_time.callback_query(Text("_plus_n_sec_pressed_"))
async def plus_n_sec(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    host_data['settings']['toast_time'] += 10
    toast_time = host_data['settings']['toast_time']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Toast time:']} {toast_time}",
                                     reply_markup=host_keyboards.set_toast_time_inline_kb())


@router_set_toast_time.callback_query(Text("_minus_n_sec_pressed_"))
async def minus_n_sec(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    if host_data['settings']['toast_time'] <= 11:
        return await callback.answer(text=HOST_LEXICON["Exception toast time"], show_alert=True)
    host_data['settings']['toast_time'] -= 10
    toast_time = host_data['settings']['toast_time']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Toast time:']} {toast_time}",
                                     reply_markup=host_keyboards.set_toast_time_inline_kb())


@router_set_toast_time.callback_query(Text("_exit_settings_menu_pressed_"))
async def exit_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await game_settings(callback, state, bot)
