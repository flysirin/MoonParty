import io
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from keyboards import host_keyboards
from models.methods import get_user_data
from config_data.config import host_game_data
from lexicon.lexicon import HOST_LEXICON
from random import randint
import qrcode
import logging


def make_qr_code(text: str) -> BufferedInputFile:
    img = qrcode.make(text)
    byte_stream = io.BytesIO()
    img.save(byte_stream)
    img_bytes = byte_stream.getvalue()
    img_send = BufferedInputFile(file=img_bytes, filename="img_1.png")
    return img_send


def get_authorization_qr_code(username: str, code: str | int) -> BufferedInputFile:
    code_text = f"https://t.me/Moon_Party_Bot?start={username}_{code}"
    return make_qr_code(code_text)


async def send_curr_qr_code(chat_id: int, host_username: str, state: FSMContext, bot: Bot):
    auth_code = (await state.get_data()).get('cur_code', False)
    if not auth_code:
        auth_code = randint(1111111, 9999999)
        await state.update_data(cur_code=auth_code)
    qr_code: BufferedInputFile = get_authorization_qr_code(username=host_username, code=auth_code)
    await bot.send_photo(chat_id=chat_id, photo=qr_code, caption=HOST_LEXICON["QR code to enter the game"],
                         reply_markup=host_keyboards.hide_qr_inline_kb())


async def get_game_info(host_id: int, bot: Bot):
    leader_data = await get_user_data(bot, host_id)
    players = leader_data.get('players', {})
    players_info = f"{HOST_LEXICON['Players info']}\n"
    for player_id, player_data in players.items():
        nickname = player_data.get('nickname', 0)
        lives = [0, player_data.get('lives', 0)][player_data.get('lives', 0) > 0]
        role = player_data.get('role', '')
        is_werewolf = ['', HOST_LEXICON['werewolf']][bool(player_data.get('is_werewolf', ''))]
        is_speaker = ['', HOST_LEXICON['Speaker']][leader_data.get('current_speaker', 0) == player_id]

        players_info += f"{nickname} | {HOST_LEXICON['lives:']} {lives} |" \
                        f" {HOST_LEXICON['role:']} {role} | {is_werewolf} | " \
                        f"{is_speaker}\n"
    return players_info


async def update_qr_code_data(state: FSMContext):
    await state.update_data(cur_code=randint(1111111, 9999999))


async def reset_game_settings(state: FSMContext):
    await state.update_data(data=host_game_data)
