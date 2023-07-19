import asyncio

from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import bot_object
from states.host_states import FSMHost

from aiogram.filters import Command, CommandStart, StateFilter, Text
from filters.member_filters import IsHost

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import host_keyboards

from lexicon.lexicon import HOST_LEXICON, HOST_BOTTOMS

from services import game, user_services
import logging

logging.basicConfig(level=logging.INFO)
logger_host = logging.getLogger(__name__)

router_host = Router()
router_host.message.filter(IsHost())
router_host.callback_query.filter(IsHost())


@router_host.callback_query(~Text(["_start_game_pressed_", "_finish_game_pressed_"]), StateFilter(FSMHost.game_process))
async def exception_game_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=HOST_LEXICON['Message state of play'])


@router_host.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=f"{HOST_LEXICON['Room name: ']}{(await state.get_data()).get('room_name', '')}\n"
                              f"{HOST_LEXICON['Password: ']}{(await state.get_data()).get('password', '')}",
                         reply_markup=host_keyboards.host_inline_kb())
    await state.set_state(None)


# --> Handlers for change room name and password
@router_host.callback_query(Text("change_room_name_pressed"))
async def change_room_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMHost.input_room_name)
    await callback.message.answer(text=HOST_LEXICON['Waiting for a room name:'])


@router_host.message(F.text, StateFilter(FSMHost.input_room_name))
async def input_room_name(message: Message, state: FSMContext):
    await state.update_data(room_name=message.text)
    await message.answer(text=f"{HOST_LEXICON['Room name: ']}{(await state.get_data()).get('room_name', '')}\n"
                              f"{HOST_LEXICON['Password: ']}{(await state.get_data()).get('password', '')}",
                         reply_markup=host_keyboards.host_inline_kb())
    await state.set_state(None)


@router_host.callback_query(Text("change_pass_pressed"))
async def change_password(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"Waiting for a password: ")
    await state.set_state(FSMHost.input_password)


@router_host.message(F.text, StateFilter(FSMHost.input_password))
async def input_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer(text=f"{HOST_LEXICON['Room name: ']}{(await state.get_data()).get('room_name', '')}\n"
                              f"{HOST_LEXICON['Password: ']}{(await state.get_data()).get('password', '')}",
                         reply_markup=host_keyboards.host_inline_kb())
    await state.set_state(None)


# <-- End handlers for change room name and password


# --> Handlers for game process
@router_host.callback_query(Text("init_game_pressed"))
async def init_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # await game.clear_data_game(host_id=callback.from_user.id, bot=bot)

    data = await state.get_data()
    if not (data.get('room_name', '') and data.get('password', '')):
        return await callback.answer(text=HOST_LEXICON["Can't start without Room Name or pass"])
    players = data.get('players', {})
    await callback.message.answer(text=HOST_LEXICON["Message waiting players"],
                                  reply_markup=host_keyboards.registered_players_inline_kb(**players))
    await state.set_state(FSMHost.wait_register_players)
    await state.update_data(active_registration=True)
    await callback.answer()


@router_host.callback_query(Text("_update_user_lists_"), StateFilter(FSMHost.wait_register_players))
async def update_user_list(callback: CallbackQuery, state: FSMContext):
    players = (await state.get_data()).get('players', {})
    await callback.message.answer(text=HOST_LEXICON["Message waiting players"],
                                  reply_markup=host_keyboards.registered_players_inline_kb(**players))
    await callback.message.delete()
    await callback.answer()


@router_host.callback_query(Text("_start_game_pressed_"))
async def start_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # await game.clear_data_game(host_id=callback.from_user.id, bot=bot)

    players = (await state.get_data()).get('players', {})
    if not len(players) >= 1:
        return await callback.message.answer(text=HOST_LEXICON["Unable to start"])

    # await callback.answer(text=f"Start game pressed")
    await state.update_data(active_registration=False)
    await state.update_data(active_game=True)

    await callback.message.answer(text=HOST_BOTTOMS["Game menu: "],
                                  reply_markup=host_keyboards.game_process_menu(**players))
    await state.set_state(FSMHost.game_process)
    await game.start_init_players(host_id=callback.from_user.id)
    await game.game_process(host_id=callback.from_user.id, bot=bot)


@router_host.callback_query(Text("_finish_game_pressed_"), StateFilter(FSMHost.game_process))
async def start_game_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # await callback.message.answer(text=f"{HOST_LEXICON['Game data cleared']}")
    await update_user_list(callback, state)
    # await state.update_data(active_registration=False)
    await state.update_data(active_game=False)

    await game.clear_data_game(host_id=callback.from_user.id, bot=bot)

    await state.set_state(FSMHost.wait_register_players)


# <-- End handlers for game process


########################################################################################################################
@router_host.callback_query(Text("_cancel_all_data_"))
async def cancel_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text=f"{HOST_LEXICON['Room name: ']}{(await state.get_data()).get('room_name', '')}\n"
             f"{HOST_LEXICON['Password: ']}{(await state.get_data()).get('password', '')}",
        reply_markup=callback.message.reply_markup)
    await callback.answer(text=HOST_LEXICON["All data canceled"])


@router_host.message(Command(commands=["cancel"]))
async def command_cancel(message: Message, state: FSMContext, bot: Bot):
    # await message.delete()
    # await bot.delete_my_commands()
    await message.answer(text=HOST_LEXICON["States canceled"], reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)


@router_host.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=HOST_LEXICON["/help"])


@router_host.callback_query()
async def test_callback(callback: CallbackQuery):
    await callback.answer(text=f"from router_host callback data: {callback.data}")
