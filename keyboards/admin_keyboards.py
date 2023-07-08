from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder


# from lexicon.lexicon import LEXICON

def admin_kb() -> ReplyKeyboardMarkup:
    ad_room_leader_button = KeyboardButton(text="Add room leader")
    show_room_leaders_button = KeyboardButton(text="Show room leaders")
    create_room_button = KeyboardButton(text="Create room for game")
    delete_all_data_button = KeyboardButton(text="Delete all data!")

    keyboard = ReplyKeyboardMarkup(keyboard=[[ad_room_leader_button],
                                             [show_room_leaders_button],
                                             [delete_all_data_button],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def confirm_add_leaders_kb() -> InlineKeyboardMarkup:
    confirm_user_button = InlineKeyboardButton(text="Confirm add leader",
                                               callback_data="confirm_add_room_leader")
    cancel_button = InlineKeyboardButton(text="Cancel operation",
                                         callback_data="##cancel##operation##")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_user_button],
                                                     [cancel_button], ])
    return keyboard


def cancel_all_data_kb() -> InlineKeyboardMarkup:
    confirm_delete_all_data_button = InlineKeyboardButton(text="Attention! Cancel ALL data!!!",
                                                          callback_data="confirm_cancel_all_data(!)")
    cancel_operation_button = InlineKeyboardButton(text="Cancel operation",
                                                   callback_data="##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_delete_all_data_button],
                                                     [cancel_operation_button], ])
    return keyboard


def show_room_leaders_inline_kb(width: int = 1, **kwargs: dict) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for nickname, annotation in kwargs.items():
            user_id = annotation.get('user_id', 0)
            buttons.append(InlineKeyboardButton(text=f"{nickname}   |   User_id? -> "
                                                     f"{['Not set', f'{user_id}'][bool(user_id)]}",
                                                callback_data=f"__{nickname}__"))

    kb_builder.row(*buttons, width=width)  # unpack button's list to builder by method row with param width

    return kb_builder.as_markup()  # return object inline kb


def set_options_for_room_leader_kb(nickname: str) -> InlineKeyboardMarkup:
    show_statistic_button = InlineKeyboardButton(text=f"Show statistic",
                                                 callback_data=f"##show_statistic##{nickname}##")
    delete_leader_button = InlineKeyboardButton(text=f"Delete leader",
                                                callback_data=f"##delete##{nickname}##")
    cancel_operation_button = InlineKeyboardButton(text=f"Cancel operation",
                                                   callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[show_statistic_button],
                                                     [delete_leader_button],
                                                     [cancel_operation_button]])
    return keyboard


def confirm_delete_room_leader_kb(nickname: str) -> InlineKeyboardMarkup:
    confirm_delete_room_leader_button = InlineKeyboardButton(text=f"Confirm delete",
                                                             callback_data=f"##confirm##delete##{nickname}##")
    cancel_operation_button = InlineKeyboardButton(text=f"Cancel operation",
                                                   callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_delete_room_leader_button],
                                                     [cancel_operation_button]])
    return keyboard


def cancel_state_admin_kb() -> InlineKeyboardMarkup:
    cancel_state_button = InlineKeyboardButton(text="Cancel",
                                               callback_data="##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])
    return keyboard
