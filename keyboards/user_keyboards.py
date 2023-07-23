from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import USER_BUTTONS


def start_kb() -> ReplyKeyboardMarkup:
    show_active_rooms = KeyboardButton(text=USER_BUTTONS["Show active rooms"])
    set_nickname = KeyboardButton(text=USER_BUTTONS["Set nickname"])
    # cancel_state = KeyboardButton(text=USER_LEXICON["Click to exit"])
    keyboard = ReplyKeyboardMarkup(keyboard=[[show_active_rooms],
                                             [set_nickname],
                                             # [cancel_state],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def active_rooms_inline_kb(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for room_name, host_id in kwargs.items():
            buttons.append(InlineKeyboardButton(text=f"{room_name}",
                                                callback_data=f"__{room_name}__name__{host_id}__id__"))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb


def user_game_kb() -> InlineKeyboardMarkup:
    change_role = InlineKeyboardButton(text=USER_BUTTONS["Change role"],
                                       callback_data=f"##change##role##pressed##")
    show_your_role = InlineKeyboardButton(text=USER_BUTTONS["Show your role"],
                                          callback_data=f"##show##role##pressed##")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[change_role],
                                                     [show_your_role],
                                                     ])
    return keyboard


def cancel_operation() -> InlineKeyboardMarkup:
    cancel = InlineKeyboardButton(text=USER_BUTTONS["Click to exit"],
                                  callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel]])
    return keyboard

# def input_pass_inline_kb(room_name) -> InlineKeyboardMarkup:
#     input_pass = InlineKeyboardButton(text=f"{USER_LEXICON['Input password: ']}{room_name} ",
#                                       callback_data=f"__{room_name}__input_password__")
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[input_pass]])
#     return keyboard
