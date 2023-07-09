from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


def start_kb() -> ReplyKeyboardMarkup:
    show_active_rooms = KeyboardButton(text="Show active rooms")

    keyboard = ReplyKeyboardMarkup(keyboard=[[show_active_rooms],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def active_rooms(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for room_name, annotation in kwargs.items():

            buttons.append(InlineKeyboardButton(text=f"{room_name}",
                                                callback_data=f"__{room_name}__"))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb
