from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder


# from lexicon.lexicon import LEXICON

def admin_kb() -> ReplyKeyboardMarkup:
    ad_admin_room_button = KeyboardButton(text="Add room admin")
    show_admin_rooms_button = KeyboardButton(text="Show room admins")
    create_room_button = KeyboardButton(text="Create room for game")
    delete_all_data_button = KeyboardButton(text="Delete all data!")

    keyboard = ReplyKeyboardMarkup(keyboard=[[ad_admin_room_button],
                                             [show_admin_rooms_button],
                                             [delete_all_data_button],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def confirm_add_to_admins_kb() -> InlineKeyboardMarkup:
    confirm_user_button = InlineKeyboardButton(text="Confirm to add admin room",
                                               callback_data="confirm_add_admin_room")
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


def show_room_admins_inline_kb(width: int = 1, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for nickname, annotation in kwargs.items():
            buttons.append(InlineKeyboardButton(text=f"{nickname}   |   Is set user_id? -> "
                                                     f"{['No', f'{annotation}'][bool(annotation)]}",
                                                callback_data=f"__{nickname}__"))

    kb_builder.row(*buttons, width=width)  # unpack button's list to builder by method row with param width

    return kb_builder.as_markup()  # return object inline kb


def set_options_for_admin_room_kb(nickname: str) -> InlineKeyboardMarkup:
    show_statistic_button = InlineKeyboardButton(text=f"Show statistic",
                                                 callback_data=f"##show_statistic##{nickname}##")
    delete_admin_button = InlineKeyboardButton(text=f"Delete admin",
                                               callback_data=f"##delete##{nickname}##")
    cancel_operation_button = InlineKeyboardButton(text=f"Cancel operation",
                                                   callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[show_statistic_button],
                                                     [delete_admin_button],
                                                     [cancel_operation_button]])
    return keyboard


def confirm_delete_admin_room_kb(nickname: str) -> InlineKeyboardMarkup:
    confirm_delete_admin_room_button = InlineKeyboardButton(text=f"Confirm delete",
                                                            callback_data=f"##confirm##delete##{nickname}##")
    cancel_operation_button = InlineKeyboardButton(text=f"Cancel operation",
                                                   callback_data=f"##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_delete_admin_room_button],
                                                     [cancel_operation_button]])
    return keyboard



def cancel_state_admin_kb() -> InlineKeyboardMarkup:
    cancel_state_button = InlineKeyboardButton(text="Cancel",
                                               callback_data="##cancel##operation##")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])
    return keyboard

# def admin_room_inline_kb() -> InlineKeyboardMarkup:
#     game_process = InlineKeyboardButton(text="Start Game", callback_data="start_game_pressed")
#     room_name = InlineKeyboardButton(text="Change room name", callback_data="change_room_name_pressed")
#     change_pass = InlineKeyboardButton(text="Change password", callback_data="change_pass_pressed")
#     game_setting = InlineKeyboardButton(text="Game setting", callback_data="setting_game_pressed")
#     cancel_state = InlineKeyboardButton(text="Cancel state", callback_data="cancel_state")
#     cancel_data = InlineKeyboardButton(text="Cancel data", callback_data="cancel_data")
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[game_process],
#                                                      [room_name],
#                                                      [change_pass],
#                                                      [game_setting],
#                                                      [cancel_state],
#                                                      [cancel_data]], )
#     return keyboard


# def create_admin_room_kb() -> ReplyKeyboardMarkup:
#     start_game_button = KeyboardButton(text="Start")
#     finish_game_button = KeyboardButton(text="Finish game")
#     set_storage_data = KeyboardButton(text="Set data storage")
#     get_storage_data = KeyboardButton(text="Get data storage")
#
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[[start_game_button],
#                   [finish_game_button],
#                   [get_storage_data],
#                   [set_storage_data],
#                   ],
#         resize_keyboard=True,
#         one_time_keyboard=True)
#
#     return keyboard
