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

router_start_menu = Router()


# start menu
@router_start_menu.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    await message.answer(text=HOST_LEXICON["Choose an option"],
                         reply_markup=host_keyboards.main_menu_inline_kb())
    await state.set_state(None)


@router_start_menu.callback_query(Text("init_game_pressed"))
async def init_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await host_services.send_curr_qr_code(chat_id=callback.from_user.id,
                                          host_username=callback.from_user.username,
                                          state=state, bot=bot)
    players = (await state.get_data()).get('players', {})
    await callback.message.answer(text=f"{HOST_LEXICON['Waiting for players to register']} {len(players)}",
                                  reply_markup=host_keyboards.registered_players_inline_kb())
    await state.set_state(FSMHost.wait_register_players)
    await state.update_data(active_registration=True)
    await callback.message.delete()
