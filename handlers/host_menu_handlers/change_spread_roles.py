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

router_change_spread_roles = Router()
router_change_spread_roles.callback_query.filter(StateFilter(FSMHost.change_spread_roles))


@router_change_spread_roles.callback_query(Text(startswith=["_plus_spread_", "_minus_spread_"]))
async def change_spread(callback: CallbackQuery, state: FSMContext, bot: Bot):
    spread_roles = (await state.get_data()).get('change_spread_roles', {'human': 40, 'wolf': 40, 'werewolf': 20})

    callback_data = callback.data
    if callback_data == "_plus_spread_wolf_pressed_":
        if spread_roles['wolf'] >= 90:
            return await callback.answer(text=HOST_LEXICON["Exception spread role 90"])
        spread_roles['wolf'] += 10
    elif callback_data == "_minus_spread_wolf_pressed_":
        if spread_roles['wolf'] <= 0:
            return await callback.answer()
        spread_roles['wolf'] -= 10

    elif callback_data == "_plus_spread_human_pressed_":
        if spread_roles['human'] >= 90:
            return await callback.answer(text=HOST_LEXICON["Exception spread role 90"])
        spread_roles['human'] += 10
    elif callback_data == "_minus_spread_human_pressed_":
        if spread_roles['human'] <= 0:
            return await callback.answer()
        spread_roles['human'] -= 10

    elif callback_data == "_plus_spread_werewolf_pressed_":
        if spread_roles['werewolf'] >= 90:
            return await callback.answer(text=HOST_LEXICON["Exception spread role 90"])
        spread_roles['werewolf'] += 10
    elif callback_data == "_minus_spread_werewolf_pressed_":
        if spread_roles['werewolf'] <= 0:
            return await callback.answer()
        spread_roles['werewolf'] -= 10

    sum_percent_roles = spread_roles['werewolf'] + spread_roles['human'] + spread_roles['wolf']
    _flag = ['🚫', '✅'][sum_percent_roles == 100]

    info = f"{HOST_LEXICON['human']} / {HOST_LEXICON['wolf']} / {HOST_LEXICON['werewolf']}\n" \
           f"    {spread_roles['human']}%      /   {spread_roles['wolf']}%   /      {spread_roles['werewolf']}%"\
           f"\n{HOST_LEXICON['Sum percent roles:']} {sum_percent_roles} {_flag}"

    try:
        await callback.message.edit_text(text=f"{HOST_LEXICON['Spread roles']}\n\n <b>{info}</b>",
                                         reply_markup=host_keyboards.spread_roles_inline_kb())
    except BaseException as e:
        await callback.answer()
    await state.update_data(change_spread_roles=spread_roles)


@router_change_spread_roles.callback_query(Text("_confirm_spread_setting_pressed_"))
async def confirm_spread_roles(callback: CallbackQuery, state: FSMContext, bot: Bot):
    host_data = await state.get_data()
    spread_roles = (await state.get_data()).get('change_spread_roles', {})
    if (spread_roles['human'] + spread_roles['wolf'] + spread_roles['werewolf']) != 100:
        return await callback.answer(text=HOST_LEXICON['Exception spread role'], show_alert=True)

    host_data['settings']['percent_role'] = spread_roles
    await state.update_data(data=host_data)
    info = f"{HOST_LEXICON['human']} / {HOST_LEXICON['wolf']} / {HOST_LEXICON['werewolf']}\n" \
           f"    {spread_roles['human']}%     /   {spread_roles['wolf']}%   /     {spread_roles['werewolf']}%"

    try:
        await callback.message.edit_text(text=f"{HOST_LEXICON['Spread roles']}\n\n <b>{info}</b>",
                                         reply_markup=host_keyboards.spread_roles_inline_kb())
    except BaseException as e:
        await callback.answer()


@router_change_spread_roles.callback_query(Text("_exit_settings_menu_pressed_"))
async def exit_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await game_settings(callback, state, bot)
