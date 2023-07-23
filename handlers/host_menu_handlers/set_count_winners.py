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

router_set_count_winners = Router()
router_set_count_winners.callback_query.filter(StateFilter(FSMHost.set_count_winners))


@router_set_count_winners.callback_query(Text("_plus_one_pressed_"))
async def plus_n_sec(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    host_data['settings']['count_winners'] += 1
    count_winners = host_data['settings']['count_winners']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Count winners:']} {count_winners}",
                                     reply_markup=host_keyboards.count_winners_inline_kb())


@router_set_count_winners.callback_query(Text("_minus_one_pressed_"))
async def minus_n_sec(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    if host_data['settings']['count_winners'] < 2:
        return await callback.answer(text=HOST_LEXICON["Exception count winners"], show_alert=True)
    host_data['settings']['count_winners'] -= 1
    count_winners = host_data['settings']['count_winners']
    await state.update_data(data=host_data)
    await callback.message.edit_text(text=f"{HOST_LEXICON['Count winners:']} {count_winners}",
                                     reply_markup=host_keyboards.count_winners_inline_kb())


@router_set_count_winners.callback_query(Text("_exit_settings_menu_pressed_"))
async def exit_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await game_settings(callback, state, bot)
