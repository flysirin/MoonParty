import io
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
import logging
import qrcode
from random import randint
from lexicon.lexicon import HOST_LEXICON
from keyboards import host_keyboards

async def delete_last_message(chat_id: int, state: FSMContext, bot: Bot):
    try:
        cur_message_id = (await state.get_data()).get('cur_message_id', 0)
        await bot.delete_message(chat_id=chat_id, message_id=cur_message_id)
    except BaseException as e:
        logging.getLogger(__name__).error(f"Exception delete message: {e}")


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
    code = (await state.get_data()).get('cur_code', False)
    if not code:
        code = randint(1111111, 9999999)
        await state.update_data(cur_code=code)
    qr_code: BufferedInputFile = get_authorization_qr_code(username=host_username, code=code)
    await bot.send_photo(chat_id=chat_id, photo=qr_code, caption=HOST_LEXICON["QR code to enter the game"],
                         reply_markup=host_keyboards.hide_qr_inline_kb())

