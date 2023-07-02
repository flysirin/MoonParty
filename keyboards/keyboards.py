from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, )

# from lexicon.lexicon import LEXICON


def create_inline_kb(*args, **kwargs) -> InlineKeyboardMarkup:
    read_text_button: InlineKeyboardButton = InlineKeyboardButton(
        text="Press for read text",
        callback_data="read_text_button_pressed")
    send_text_open_ai_button: InlineKeyboardButton = InlineKeyboardButton(
        text="Send text to AI GPT 3.5",
        callback_data="send_text_open_ai"
    )
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[read_text_button],
                         [send_text_open_ai_button]])
    return keyboard


def create_admin_room_kb() -> ReplyKeyboardMarkup:
    start_game_button = KeyboardButton(text="Start game")
    finish_game_button = KeyboardButton(text="Finish game")
    set_storage_data = KeyboardButton(text="Set data storage")
    get_storage_data = KeyboardButton(text="Get data storage")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[start_game_button],
                  [finish_game_button],
                  [get_storage_data],
                  [set_storage_data],
                  ],
        resize_keyboard=True,
        one_time_keyboard=True)

    return keyboard


def create_main_admin_kb() -> InlineKeyboardMarkup:
    ad_admin_room_button = InlineKeyboardButton(text="Add admin room",
                                                callback_data="add_admin_room_pressed")
    delete_admin_room_button = InlineKeyboardButton(text="Delete admin room",
                                                    callback_data="delete_admin_room_pressed")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[ad_admin_room_button],
                                              [delete_admin_room_button], ])
    return keyboard

