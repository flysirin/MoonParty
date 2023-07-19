from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.room_leader_states import FSMRoomLeader

from aiogram.filters import Command, CommandStart, StateFilter, Text
from filters.member_filters import IsRoomLeader

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards import room_leader_keyboards

from lexicon.lexicon import LEADER_LEXICON
import logging

logging.basicConfig(level=logging.INFO)
logger_leader_handler = logging.getLogger(__name__)

router_room_leader = Router()
router_room_leader.message.filter(IsRoomLeader())
router_room_leader.callback_query.filter(IsRoomLeader())


@router_room_leader.message(F.text or Command("start"), StateFilter(FSMRoomLeader.game_process))
async def exception_game_process(message: Message, state: FSMContext):
    await message.answer(text=LEADER_LEXICON['Message state of play'])


@router_room_leader.callback_query(~Text(["_start_game_pressed_", "_finish_game_pressed_"]), StateFilter(FSMRoomLeader.game_process))
async def exception_game_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEADER_LEXICON['Message state of play'])


@router_room_leader.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                              f"Password:{(await state.get_data()).get('password', '')}",
                         reply_markup=room_leader_keyboards.room_leader_inline_kb())
    await state.set_state(None)


# --> Handlers for change room name and password
@router_room_leader.callback_query(Text("change_room_name_pressed"))
async def change_room_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMRoomLeader.input_room_name)
    await callback.message.answer(text=LEADER_LEXICON['Waiting for a room name:'])


@router_room_leader.message(F.text, StateFilter(FSMRoomLeader.input_room_name))
async def input_room_name(message: Message, state: FSMContext):
    await state.update_data(room_name=message.text)
    await message.answer(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                              f"Password:{(await state.get_data()).get('password', '')}",
                         reply_markup=room_leader_keyboards.room_leader_inline_kb())
    await state.set_state(None)


@router_room_leader.callback_query(Text("change_pass_pressed"))
async def change_password(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"Waiting for a password: ")
    await state.set_state(FSMRoomLeader.input_password)


@router_room_leader.message(F.text, StateFilter(FSMRoomLeader.input_password))
async def input_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                              f"Password:{(await state.get_data()).get('password', '')}",
                         reply_markup=room_leader_keyboards.room_leader_inline_kb())
    await state.set_state(None)
# <-- End handlers for change room name and password


# --> Handlers for game process
@router_room_leader.callback_query(Text("init_game_pressed"))
async def init_game_process(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not (data.get('room_name', '') and data.get('password', '')):
        return await callback.answer(text=LEADER_LEXICON["Can't start without Room Name or pass"])
    players = data.get('players', {})
    await callback.message.answer(text=LEADER_LEXICON["Message waiting players"],
                                  reply_markup=room_leader_keyboards.registered_players_inline_kb(**players))
    await state.set_state(FSMRoomLeader.wait_register_players)
    await state.update_data(active_registration=True)
    await callback.answer()


@router_room_leader.callback_query(Text("_update_user_lists_"), StateFilter(FSMRoomLeader.wait_register_players))
async def update_user_list(callback: CallbackQuery, state: FSMContext):
    players = (await state.get_data()).get('players', {})
    await callback.message.answer(text=f"Registered players:",
                                  reply_markup=room_leader_keyboards.registered_players_inline_kb(**players))
    await callback.message.delete()
    await callback.answer()


@router_room_leader.callback_query(Text("_start_game_pressed_"))
async def start_game_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=f"Start game pressed")
    await state.update_data(active_registration=False)
    await state.set_state(FSMRoomLeader.game_process)
    players = (await state.get_data()).get('players', {})
    await callback.message.answer(text=f"Game menu: ",
                                  reply_markup=room_leader_keyboards.game_process_menu(**players))


@router_room_leader.callback_query(Text("_finish_game_pressed_"), StateFilter(FSMRoomLeader.game_process))
async def start_game_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"{LEADER_LEXICON['Game data cleared']}")
    await update_user_list(callback, state)
    await state.update_data(active_registration=False)
    await state.set_state(FSMRoomLeader.wait_register_players)
    # await callback.message.answer(text=f"")
# <-- End handlers for game process


########################################################################################################################
@router_room_leader.callback_query(Text("_cancel_all_data_"))
async def cancel_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=f"Room name: {(await state.get_data()).get('room_name', '')}\n"
                                          f"Password:{(await state.get_data()).get('password', '')}",
                                     reply_markup=callback.message.reply_markup)
    await callback.answer(text="All data canceled")


@router_room_leader.message(Command("cancel"))
async def command_cancel(message: Message, state: FSMContext, bot: Bot):
    # await message.delete()
    # await bot.delete_my_commands()
    await message.answer(text="States canceled", reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)


@router_room_leader.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=LEADER_LEXICON["/help"])


@router_room_leader.callback_query()
async def test_callback(callback: CallbackQuery):
    await callback.answer(text=f"from router_leader callback data: {callback.data}")
