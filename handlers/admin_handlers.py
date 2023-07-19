from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.admin_states import FSMAdmin

from aiogram.filters import Command, CommandStart, StateFilter, Text, or_f
from filters.member_filters import IsMainAdmins

from aiogram.types import Message, CallbackQuery
from keyboards import admin_keyboards

from lexicon.lexicon import ADMIN_LEXICON, ADMIN_BOTTOMS
import logging

logging.basicConfig(level=logging.INFO)
logger_admin_handler = logging.getLogger(__name__)

router_admin = Router()
router_admin.message.filter(IsMainAdmins())
router_admin.callback_query.filter(IsMainAdmins())


@router_admin.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    logger_admin_handler.info(f"Command start for main admins, id: {message.from_user.id}")
    message = await message.answer(text=ADMIN_LEXICON["/start"],
                                   reply_markup=admin_keyboards.admin_kb())
    await state.update_data(cur_message_id=message.message_id)
    await state.set_state(None)


# --> Handlers for add hosts
@router_admin.message(Text(text=ADMIN_BOTTOMS["Add host"]))
async def add_host(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(FSMAdmin.add_host)
    await message.answer(text=ADMIN_LEXICON["Input nickname"],
                         reply_markup=admin_keyboards.cancel_state_admin_kb())
    await message.delete()


@router_admin.message(or_f(Text(contains='/'), Text(startswith='@')), StateFilter(
    FSMAdmin.add_host))  # lambda message: '/' in message.text or '@' in message.text)
async def add_host(message: Message):
    nickname = message.text.split('/')[-1].split('@')[-1]
    if nickname:
        await message.answer(text=nickname,
                             reply_markup=admin_keyboards.confirm_add_hosts_kb())
        await message.delete()


@router_admin.callback_query(Text("confirm_add__host"))
async def confirm_add_host(callback: CallbackQuery, state: FSMContext):
    hosts: dict = (await state.get_data()).get('hosts', {})
    if not hosts:
        await state.update_data(data={'hosts': {}})
    hosts.update({callback.message.text: {}})

    await state.update_data(data={'hosts': hosts})
    logger_admin_handler.info(f"{callback.message.text}")

    await callback.answer(text=f"{ADMIN_LEXICON['Successful addition of game host']}{callback.message.text}\n")
    await state.set_state(None)
    await callback.message.delete()


@router_admin.message(StateFilter(FSMAdmin.add_host),
                      lambda m: m.text not in ["Cancel all data!", "Show hosts",
                                               "Delete host", "Add host", "Create room for game"])
async def another_wrong(message: Message):
    await message.answer(text=ADMIN_LEXICON['Incorrect input user'],
                         reply_markup=admin_keyboards.cancel_state_admin_kb())


# <-- End handlers for add  hosts


# --> Handlers for delete all data
@router_admin.message(Text(text=ADMIN_BOTTOMS["Delete all data!"]))
async def cancel_all_data(message: Message, state: FSMContext):
    await message.answer(text=ADMIN_LEXICON["Are you sure delete all data?!"],
                         reply_markup=admin_keyboards.cancel_all_data_kb())
    await message.delete()
    await state.set_state(None)


@router_admin.callback_query(Text("confirm_cancel_all_data(!)"))
async def confirm_delete_all_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(text=ADMIN_LEXICON["All data was deleted!"])
    await callback.message.delete()


# <-- End handlers for delete all data


# --> Handlers for show and delete  hosts
@router_admin.message(Text(text=ADMIN_BOTTOMS["Show hosts"]))
async def show_hosts(message: Message, state: FSMContext):
    hosts = (await state.get_data()).get('hosts', {})
    if not hosts:
        await message.answer(text=ADMIN_LEXICON["Hosts not set"])
    else:
        await message.answer(text=ADMIN_LEXICON["Host nicknames. Press for action."],
                             reply_markup=admin_keyboards.show_hosts_inline_kb(**hosts, width=1))
    await message.delete()
    await state.set_state(None)


@router_admin.callback_query(F.data.regexp(r"_{2}.*_{2}"))
async def get_host(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[2:-2]
    hosts = (await state.get_data()).get('hosts', {}).keys()
    if nickname in hosts:
        await callback.message.answer(text=f"{ADMIN_LEXICON['Select option for  host: ']}{nickname}",
                                      reply_markup=admin_keyboards.set_options_for_host_kb(nickname=nickname))
    await callback.answer()


# -> delete  host
@router_admin.callback_query(F.data.regexp(r"#{2}delete#{2}.*#{2}"))
async def confirm_delete_host(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[10:-2]
    await callback.message.answer(text=f"{ADMIN_LEXICON['Are you sure delete: ']}{nickname} ?",
                                  reply_markup=admin_keyboards.confirm_delete_host_kb(nickname=nickname))
    await callback.message.delete()


@router_admin.callback_query(F.data.regexp(r"#{2}confirm#{2}delete#{2}.*#{2}"))
async def delete_host(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[19:-2]
    hosts = (await state.get_data()).get("hosts", {})
    logger_admin_handler.info(f"hosts dict: {hosts}")
    logger_admin_handler.info(f"Deleted nickname: {nickname}")
    if nickname not in hosts:
        return await callback.answer(text=f"{ADMIN_LEXICON['Can not deleted: ']}{nickname}")

    hosts.pop(nickname, '')
    await state.update_data({"hosts": hosts})
    await callback.answer(text=f"{nickname} {ADMIN_LEXICON['successful deleted!']}")
    await state.set_state(None)
    await callback.message.delete()

    logger_admin_handler.info(f"All data after deleted: {(await state.get_data())}")


@router_admin.callback_query(Text("##cancel##operation##"))
async def cancel_operation_host(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer(text=ADMIN_LEXICON["Cancel operation"])
    await state.set_state(None)
    await callback.message.delete()


@router_admin.callback_query()  # test exception
async def get_host2(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=f"from router admin another callback data: {callback.data}")


# <-- End handlers for show  hosts

# -----------


@router_admin.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=ADMIN_LEXICON["/help"])
