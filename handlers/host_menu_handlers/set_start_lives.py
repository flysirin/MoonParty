from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from states.host_states import FSMHost
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import host_keyboards
from lexicon.lexicon import HOST_LEXICON, HOST_BUTTONS
from services import game, host_services
from handlers.host_menu_handlers.start_menu_handlers import game_settings
import logging

router_set_start_lives = Router()
router_set_start_lives.callback_query.filter(StateFilter(FSMHost.set_start_lives))


@router_set_start_lives.callback_query(Text("_plus_lives_pressed_"))
async def plus_n_sec(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    if host_data['settings']['start_lives'] + 5 >= host_data['settings']['win_lives']:
        return await callback.answer(text=HOST_LEXICON["Exception start lives more win"], show_alert=True)
    host_data['settings']['start_lives'] += 5
    start_lives = host_data['settings']['start_lives']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Start lives:']} {start_lives}",
                                     reply_markup=host_keyboards.set_lives_inline_kb())


@router_set_start_lives.callback_query(Text("_minus_lives_pressed_"))
async def minus_n_sec(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    if host_data['settings']['start_lives'] <= 6:
        return await callback.answer(text=HOST_LEXICON["Exception start lives"], show_alert=True)
    host_data['settings']['start_lives'] -= 5
    start_lives = host_data['settings']['start_lives']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Start lives:']} {start_lives}",
                                     reply_markup=host_keyboards.set_lives_inline_kb())


@router_set_start_lives.callback_query(Text("_exit_settings_menu_pressed_"))
async def exit_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await game_settings(callback, state, bot)
