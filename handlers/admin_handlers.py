from aiogram import Router, F, Bot

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.admin_states import FSMAdmin

from aiogram.filters import Command, CommandStart, StateFilter, Text, or_f
from filters.member_filters import IsMainAdmins

from aiogram.types import Message, CallbackQuery
from keyboards import admin_keyboards

from services.other import delete_last_message
from lexicon.lexicon import ADMIN_LEXICON, ADMIN_BOTTOMS
import logging

logging.basicConfig(level=logging.INFO)
logger_admin_handler = logging.getLogger(__name__)

router_admin = Router()
router_admin.message.filter(IsMainAdmins())
router_admin.callback_query.filter(IsMainAdmins())


@router_admin.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    logger_admin_handler.info(f"Command start for main admins, id: {message.from_user.id}")
    cur_message = await message.answer(text=ADMIN_LEXICON["/start"],
                                       reply_markup=admin_keyboards.admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await state.set_state(None)


# --> Handlers for add hosts
@router_admin.message(Text(text=ADMIN_BOTTOMS["Add host"]))
async def add_host(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)

    await state.set_state(FSMAdmin.add_host)
    cur_message = await message.answer(text=ADMIN_LEXICON["Input nickname"],
                                       reply_markup=admin_keyboards.return_admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await message.delete()


@router_admin.message(or_f(Text(contains='https://t.me/'), Text(startswith='@')), StateFilter(FSMAdmin.add_host))
async def add_host(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    nickname = message.text.split('/')[-1].split('@')[-1]
    if nickname:
        hosts: dict = (await state.get_data()).get('hosts', {})
        if not hosts:
            await state.update_data(data={'hosts': {}})
        hosts.update({nickname: {}})
        await state.update_data(data={'hosts': hosts})

        cur_message = await message.answer(text=f"{ADMIN_LEXICON['Host added:']} {nickname}",
                                           reply_markup=admin_keyboards.admin_kb())
        await state.update_data(cur_message_id=cur_message.message_id)
    await message.delete()


@router_admin.message(~Text(text=list(ADMIN_BOTTOMS.values())), StateFilter(FSMAdmin.add_host))
async def another_wrong(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    cur_message = await message.answer(text=f"{message.text}\n{ADMIN_LEXICON['Incorrect input user']}",
                                       reply_markup=admin_keyboards.return_admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await message.delete()


# <-- End handlers for add hosts


# --> Handlers for delete all data
@router_admin.message(Text(text=ADMIN_BOTTOMS["Delete all data!"]))
async def cancel_all_data(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(FSMAdmin.delete_all_data)
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    cur_message = await message.answer(text=ADMIN_LEXICON["Are you sure delete all data?!"],
                                       reply_markup=admin_keyboards.delete_all_data_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await message.delete()


@router_admin.message(Text(text=ADMIN_BOTTOMS["Confirm delete all data"]), StateFilter(FSMAdmin.delete_all_data))
async def confirm_delete_all_data(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    cur_message = await message.answer(text=ADMIN_LEXICON["All data was deleted!"],
                                       reply_markup=admin_keyboards.admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await message.delete()


# <-- End handlers for delete all data


# --> Handlers for show and delete hosts
@router_admin.message(Text(text=ADMIN_BOTTOMS["Show hosts"]))
async def show_hosts(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    hosts = (await state.get_data()).get('hosts', {})
    if not hosts:
        cur_message = await message.answer(text=ADMIN_LEXICON["Hosts not set"],
                                           reply_markup=admin_keyboards.return_admin_kb())
    else:
        cur_message = await message.answer(text=ADMIN_LEXICON["Host nicknames. Press for action."],
                                           reply_markup=admin_keyboards.show_hosts_inline_kb(**hosts, width=1))

    await state.update_data(cur_message_id=cur_message.message_id)
    await message.delete()
    await state.set_state(None)


@router_admin.callback_query(F.data.regexp(r"_{2}.*_{2}"))
async def get_host(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[2:-2]
    hosts = (await state.get_data()).get('hosts', {}).keys()
    if nickname in hosts:
        cur_message = await callback.message.answer(text=f"{ADMIN_LEXICON['Select option for host:']} {nickname}",
                                                    reply_markup=admin_keyboards.set_options_for_host_kb(
                                                        nickname=nickname))
        await state.update_data(cur_message_id=cur_message.message_id)

    await callback.message.delete()
    await callback.answer()


# -> delete  host
@router_admin.callback_query(F.data.regexp(r"#{2}delete#{2}.*#{2}"))
async def confirm_delete_host(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[10:-2]
    await callback.message.answer(text=f"{ADMIN_LEXICON['Are you sure delete:']} {nickname} ?",
                                  reply_markup=admin_keyboards.confirm_delete_host_kb(nickname=nickname))
    await callback.message.delete()


@router_admin.callback_query(F.data.regexp(r"#{2}confirm#{2}delete#{2}.*#{2}"))
async def delete_host(callback: CallbackQuery, state: FSMContext):
    nickname = callback.data[19:-2]
    hosts = (await state.get_data()).get("hosts", {})
    logger_admin_handler.info(f"hosts dict: {hosts}")
    logger_admin_handler.info(f"Deleted nickname: {nickname}")
    if nickname not in hosts:
        return await callback.answer(text=f"{ADMIN_LEXICON['Can not deleted:']} {nickname}")

    hosts.pop(nickname, '')
    await state.update_data({"hosts": hosts})
    cur_message = await callback.message.answer(text=f"{nickname} {ADMIN_LEXICON['successful deleted!']}",
                                                reply_markup=admin_keyboards.admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await state.set_state(None)
    await callback.message.delete()

    logger_admin_handler.info(f"All data after deleted: {(await state.get_data())}")


@router_admin.callback_query(Text("##cancel##operation##"))
async def cancel_operation_host(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=callback.message.from_user.id, state=state, bot=bot)
    cur_message = await callback.message.answer(text=ADMIN_LEXICON["/start"],
                                                reply_markup=admin_keyboards.admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)
    await callback.message.delete()
    await state.set_state(None)


@router_admin.message(Text(text=ADMIN_BOTTOMS["Return"]))
async def return_main_menu(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    cur_message = await message.answer(text=ADMIN_LEXICON["/start"],
                                       reply_markup=admin_keyboards.admin_kb())
    await message.delete()
    await state.update_data(cur_message_id=cur_message.message_id)
    await state.set_state(None)


@router_admin.callback_query()  # test exception
async def get_host2(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=f"from router admin another callback data: {callback.data}")


# <-- End handlers for show  hosts

# -----------

@router_admin.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext, bot: Bot):
    await delete_last_message(chat_id=message.from_user.id, state=state, bot=bot)
    await message.delete()
    cur_message = await message.answer(text=ADMIN_LEXICON["/help"],
                                       reply_markup=admin_keyboards.admin_kb())
    await state.update_data(cur_message_id=cur_message.message_id)

# @router_admin.callback_query(Text("confirm_add_host"))
# async def confirm_add_host(callback: CallbackQuery, state: FSMContext):
#     hosts: dict = (await state.get_data()).get('hosts', {})
#     if not hosts:
#         await state.update_data(data={'hosts': {}})
#     hosts.update({callback.message.text: {}})
#     await state.update_data(data={'hosts': hosts})
#     logger_admin_handler.info(f"{callback.message.text}")
#     await callback.answer(text=f"{ADMIN_LEXICON['Host added: ']}{callback.message.text}\n")
#     await state.set_state(None)
#     await callback.message.delete()
