from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import ADMIN_BOTTOMS


def admin_kb() -> ReplyKeyboardMarkup:
    ad_host_button = KeyboardButton(text=ADMIN_BOTTOMS["Add host"])
    show_hosts_button = KeyboardButton(text=ADMIN_BOTTOMS["Show hosts"])
    # create_room_button = KeyboardButton(text=ADMIN_BOTTOMS["Create room for game"])
    delete_all_data_button = KeyboardButton(text=ADMIN_BOTTOMS["Delete all data!"])

    keyboard = ReplyKeyboardMarkup(keyboard=[[ad_host_button],
                                             [show_hosts_button],
                                             # [create_room_button],
                                             [delete_all_data_button],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def show_hosts_inline_kb(width: int = 1, **kwargs: dict) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for nickname, annotation in kwargs.items():
            # user_id = annotation.get('user_id', 0)
            buttons.append(InlineKeyboardButton(text=f"{ADMIN_BOTTOMS['Host:']} {nickname}",
                                                callback_data=f"__{nickname}__"))
        buttons.append(InlineKeyboardButton(text=ADMIN_BOTTOMS["Cancel operation"],
                                            callback_data=f"##cancel##operation##"))

    kb_builder.row(*buttons, width=width)  # unpack button's list to builder by method row with param width

    return kb_builder.as_markup()  # return object inline kb


def set_options_for_host_kb(nickname: str) -> InlineKeyboardMarkup:
    show_statistic_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Show statistic"],
                                                 callback_data=f"##show_statistic##{nickname}##")
    delete_host_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Delete host"],
                                              callback_data=f"##delete##{nickname}##")
    cancel_operation_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Cancel operation"],
                                                   callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[show_statistic_button],
                                                     [delete_host_button],
                                                     [cancel_operation_button]])
    return keyboard


def confirm_delete_host_kb(nickname: str) -> InlineKeyboardMarkup:
    confirm_delete_host_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Confirm delete"],
                                                      callback_data=f"##confirm##delete##{nickname}##")
    cancel_operation_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Cancel operation"],
                                                   callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_delete_host_button],
                                                     [cancel_operation_button]])
    return keyboard


def return_admin_kb() -> ReplyKeyboardMarkup:
    return_button = KeyboardButton(text=ADMIN_BOTTOMS["Return"])

    keyboard = ReplyKeyboardMarkup(keyboard=[[return_button],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def cancel_state_admin_kb() -> InlineKeyboardMarkup:
    cancel_state_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Cancel"],
                                               callback_data="##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])
    return keyboard


def delete_all_data_kb() -> ReplyKeyboardMarkup:
    delete_all_data = KeyboardButton(text=ADMIN_BOTTOMS["Confirm delete all data"])
    return_button = KeyboardButton(text=ADMIN_BOTTOMS["Return"])

    keyboard = ReplyKeyboardMarkup(keyboard=[[delete_all_data],
                                             [return_button],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard

# def confirm_add_hosts_kb() -> InlineKeyboardMarkup:
#     confirm_user_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Confirm add host"],
#                                                callback_data="confirm_add_host")
#     cancel_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Cancel operation"],
#                                          callback_data="##cancel##operation##")
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_user_button],
#                                                      [cancel_button], ])
#     return keyboard


# def cancel_all_data_kb() -> InlineKeyboardMarkup:
#     confirm_delete_all_data_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Attention! Cancel ALL data!"],
#                                                           callback_data="confirm_cancel_all_data(!)")
#     cancel_operation_button = InlineKeyboardButton(text=ADMIN_BOTTOMS["Cancel operation"],
#                                                    callback_data="##cancel##operation##")
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_delete_all_data_button],
#                                                      [cancel_operation_button], ])
#     return keyboard
