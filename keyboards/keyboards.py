from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, )


# from lexicon.lexicon import LEXICON

def admin_kb() -> ReplyKeyboardMarkup:
    ad_admin_room_button = KeyboardButton(text="Add room admin")
    delete_admin_room_button = KeyboardButton(text="Delete room admin")
    show_admin_rooms = KeyboardButton(text="Show room admins")
    # cancel_state = KeyboardButton(text="Cancel state")
    cancel_all_data = KeyboardButton(text="Cancel all data!")

    keyboard = ReplyKeyboardMarkup(keyboard=[[ad_admin_room_button],
                                             [delete_admin_room_button],
                                             [show_admin_rooms],
                                             # [cancel_state],
                                             [cancel_all_data],
                                             ],
                                   resize_keyboard=True,
                                   on_time_keyboard=True)
    return keyboard


def create_admin_room_kb() -> ReplyKeyboardMarkup:
    start_game_button = KeyboardButton(text="Start")
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


def admin_room_inline_kb() -> InlineKeyboardMarkup:
    game_process = InlineKeyboardButton(text="Start Game", callback_data="start_game_pressed")
    room_name = InlineKeyboardButton(text="Change room name", callback_data="change_room_name_pressed")
    change_pass = InlineKeyboardButton(text="Change password", callback_data="change_pass_pressed")
    game_setting = InlineKeyboardButton(text="Game setting", callback_data="setting_game_pressed")
    cancel_state = InlineKeyboardButton(text="Cancel state", callback_data="cancel_state")
    cancel_data = InlineKeyboardButton(text="Cancel data", callback_data="cancel_data")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[game_process],
                                                     [room_name],
                                                     [change_pass],
                                                     [game_setting],
                                                     [cancel_state],
                                                     [cancel_data]], )
    return keyboard


def confirm_add_to_admins() -> InlineKeyboardMarkup:
    confirm_user = InlineKeyboardButton(text="Confirm to add admin room",
                                        callback_data="confirm_add_admin_room")
    cancel = InlineKeyboardButton(text="Cancel",
                                  callback_data="cancel_confirm_add_admin")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_user],
                                                     [cancel], ])
    return keyboard


def cancel_state_admin() -> InlineKeyboardMarkup:
    cancel = InlineKeyboardButton(text="Cancel", callback_data="cancel_state_admin")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel]])
    return keyboard


def cancel_all_data() -> InlineKeyboardMarkup:
    confirm_delete_all_data = InlineKeyboardButton(text="Attention! Cancel ALL data!!!",
                                                   callback_data="confirm_cancel_all_data(!)")
    cancel = InlineKeyboardButton(text="Cancel operation",
                                  callback_data="cancel_delete_all_data")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_delete_all_data],
                                                     [cancel], ])
    return keyboard
