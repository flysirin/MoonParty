from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.admin_states import FSMAdmin

from aiogram.filters import Command, CommandStart, StateFilter, Text, ChatMemberUpdatedFilter, or_f
from filters.member_filters import IsRoomLeader, IsMainAdmins

from aiogram.types import Message, CallbackQuery
from keyboards import admin_keyboards

from lexicon.lexicon import LEXICON
from models.methods import set_data_from_user, get_data_from_user
import logging

logging.basicConfig(level=logging.INFO)
logger_admin_handler = logging.getLogger(__name__)

router_admin = Router()
router_admin.message.filter(IsMainAdmins())


@router_admin.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    logger_admin_handler.info(f"Command start for main admins, id: {message.from_user.id}")
    await message.answer(text=LEXICON["/start_admin"],
                         reply_markup=admin_keyboards.admin_kb())
    await state.set_state(None)


# --> Handlers for add room leaders
@router_admin.message(Text("Add room leader"))
async def add_admin_room(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(FSMAdmin.add_room_leader)
    await message.answer(text="Input user's link or nickname like a @nickname with '@'",
                         reply_markup=admin_keyboards.cancel_state_admin_kb())
    await message.delete()


@router_admin.message(or_f(Text(contains='/'), Text(startswith='@')), StateFilter(
    FSMAdmin.add_room_leader))  # lambda message: '/' in message.text or '@' in message.text)
async def add_room_leader(message: Message):
    nickname = message.text.split('/')[-1].split('@')[-1]
    if nickname:
        await message.answer(text=nickname,
                             reply_markup=admin_keyboards.confirm_add_leaders_kb())
        await message.delete()


@router_admin.callback_query(Text("confirm_add_room_leader"))
async def confirm_add_room_leader(callback: CallbackQuery, state: FSMContext):
    room_leaders: dict = (await state.get_data()).get('room_leaders', {})
    if not room_leaders:
        await state.update_data(data={'room_leaders': {}})
    room_leaders.update({callback.message.text: {}})

    await state.update_data(data={'room_leaders': room_leaders})
    logger_admin_handler.info(f"{callback.message.text}")

    await callback.answer(text=f"User: {callback.message.text}\n successful added")
    await state.set_state(None)
    await callback.message.delete()


@router_admin.message(StateFilter(FSMAdmin.add_room_leader),
                      lambda m: m.text not in ["Cancel all data!", "Show room leaders",
                                               "Delete room leader", "Add room leader", "Create room for game"])
async def another_wrong(message: Message):
    await message.answer(text=f"Wait input user. Incorrect input user: {message.text}\n"
                              f"Input user's link https://t.me/nick*** or nickname like a @nickname with '@'",
                         reply_markup=admin_keyboards.cancel_state_admin_kb())
# <-- End handlers for add room leaders


# --> Handlers for delete all data
@router_admin.message(Text("Delete all data!"))
async def cancel_all_data(message: Message, state: FSMContext):
    await message.answer(text="Are you sure delete all data?!",
                         reply_markup=admin_keyboards.cancel_all_data_kb())
    await message.delete()
    await state.set_state(None)


@router_admin.callback_query(Text("confirm_cancel_all_data(!)"))
async def confirm_delete_all_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(text=f"All data was deleted!")
    await callback.message.delete()
# <-- End handlers for delete all data


# --> Handlers for show and delete room leaders
@router_admin.message(Text("Show room leaders"))
async def show_room_leaders(message: Message, state: FSMContext):
    room_leaders = (await state.get_data()).get('room_leaders', {})
    if not room_leaders:
        await message.answer(text=f"Room leaders not set")
    else:
        await message.answer(text=f"Room leader nicknames. Press for action.",
                             reply_markup=admin_keyboards.show_room_leaders_inline_kb(**room_leaders, width=1))
    await message.delete()
    await state.set_state(None)


@router_admin.callback_query(F.data.regexp(r"_{2}.*_{2}"))
async def get_room_leader(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[2:-2]
    room_leaders = (await state.get_data()).get('room_leaders', {}).keys()
    if nickname in room_leaders:
        await callback.message.answer(text=f"Select option for room leader: {nickname}",
                                      reply_markup=admin_keyboards.set_options_for_room_leader_kb(nickname=nickname))
    await callback.answer()


# -> delete room leader
@router_admin.callback_query(F.data.regexp(r"#{2}delete#{2}.*#{2}"))
async def confirm_delete_room_leader(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[10:-2]
    await callback.message.answer(text=f"Are you sure delete: {nickname} ?",
                                  reply_markup=admin_keyboards.confirm_delete_room_leader_kb(nickname=nickname))
    await callback.message.delete()


@router_admin.callback_query(F.data.regexp(r"#{2}confirm#{2}delete#{2}.*#{2}"))
async def delete_room_leader(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[19:-2]
    room_leaders = (await state.get_data()).get("room_leaders", {})
    logger_admin_handler.info(f"Room leaders dict: {room_leaders}")
    logger_admin_handler.info(f"Deleted nickname: {nickname}")
    if nickname not in room_leaders:
        return await callback.answer(text=f"Can not deleted: {nickname}")

    room_leaders.pop(nickname, '')
    await state.update_data({"room_leaders": room_leaders})
    await callback.answer(text=f"{nickname} successful deleted!")
    await state.set_state(None)
    await callback.message.delete()

    logger_admin_handler.info(f"All data after deleted: {(await state.get_data())}")


@router_admin.callback_query(Text("##cancel##operation##"))
async def cancel_operation_room_leader(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text="Cancel operation")
    await state.set_state(None)
    await callback.message.delete()


@router_admin.callback_query()  # test exception
async def get_room_leader2(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=f"{callback.data}")
# <-- End handlers for show room leaders

# -----------


@router_admin.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["/help_admin"])
