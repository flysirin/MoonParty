from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.admin_states import FSMAdmin

from aiogram.filters import Command, CommandStart, StateFilter, Text, ChatMemberUpdatedFilter, or_f
from filters.member_filters import IsRoomAdmin, IsMainAdmins

from aiogram.types import Message, CallbackQuery
from keyboards import keyboards

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
                         reply_markup=keyboards.admin_kb())
    await state.set_state(None)


@router_admin.message(Text("Show room admins"))
async def show_room_admins(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=f"{data}")
    await message.delete()
    await state.set_state(None)


# --> Handlers for add room admins
@router_admin.message(Text("Add room admin"))
async def add_admin_room(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(FSMAdmin.add_admin_room)
    await message.answer(text="Input user's link or nickname like a @nickname with '@'",
                         reply_markup=keyboards.cancel_state_admin())


@router_admin.message(or_f(Text(contains='/'), Text(startswith='@')), StateFilter(
    FSMAdmin.add_admin_room))  # lambda message: '/' in message.text or '@' in message.text)
async def add_admin_room(message: Message):
    nickname = message.text.split('/')[-1].split('@')[-1]
    if nickname:
        await message.answer(text=nickname,
                             reply_markup=keyboards.confirm_add_to_admins())
        await message.delete()


@router_admin.callback_query(Text("confirm_add_admin_room"))
async def confirm_add_admin_room(callback: CallbackQuery, state: FSMContext):
    room_admins: dict = (await state.get_data()).get('room_admins', {})
    if not room_admins:
        await state.update_data(data={'room_admins': {}})
    room_admins.update({callback.message.text: {}})

    await state.update_data(data={'room_admins': room_admins})
    logger_admin_handler.info(f"{callback.message.text}")

    await callback.answer(text=f"User: {callback.message.text}\n successful added")
    await state.set_state(None)
    await callback.message.delete()


@router_admin.callback_query(Text("cancel_confirm_add_admin"))
async def confirm_add_admin_room(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=f"Cancel added user")
    await callback.message.delete()
    await state.set_state(None)


@router_admin.callback_query(Text("cancel_state_admin"), StateFilter(FSMAdmin.add_admin_room))
async def cancel_state_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.answer(text="Cancel state")
    await callback.message.delete()


@router_admin.message(StateFilter(FSMAdmin.add_admin_room),
                      lambda m: m.text not in ["Cancel all data!", "Show room admins",
                                               "Delete room admin", "Add room admin"])
async def another_wrong(message: Message):
    await message.answer(text=f"Wait input user. Incorrect input user: {message.text}\n"
                              f"Input user's link https://t.me/nick*** or nickname like a @nickname with '@'",
                         reply_markup=keyboards.cancel_state_admin())


# <-- End handlers for add room admins


# --> Handlers for delete all data
@router_admin.message(Text("Cancel all data!"))
async def cancel_all_data(message: Message):
    await message.answer(text="Are you sure delete all data?!",
                         reply_markup=keyboards.cancel_all_data())


@router_admin.callback_query(Text("confirm_cancel_all_data(!)"))
async def confirm_delete_all_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(text=f"All data was deleted!")
    await callback.message.delete()


@router_admin.callback_query(Text("cancel_delete_all_data"))
async def cancel_delete_all_data(callback: CallbackQuery):
    await callback.message.delete()


# <-- End handlers for delete all data


# -----------

@router_admin.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["/help_admin"])
