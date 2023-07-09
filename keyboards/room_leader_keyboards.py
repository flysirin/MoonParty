from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder


from lexicon.lexicon import LEXICON


def room_leader_inline_kb() -> InlineKeyboardMarkup:
    init_game = InlineKeyboardButton(text="Register room and start waiting players", callback_data="init_game_pressed")
    room_name = InlineKeyboardButton(text="Change room name", callback_data="change_room_name_pressed")
    change_pass = InlineKeyboardButton(text="Change password", callback_data="change_pass_pressed")
    game_setting = InlineKeyboardButton(text="Game setting", callback_data="setting_game_pressed")
    cancel_state = InlineKeyboardButton(text="Cancel state", callback_data="cancel_state")
    cancel_data = InlineKeyboardButton(text="Cancel data", callback_data="_cancel_all_data_")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[init_game],
                                                     [room_name],
                                                     [change_pass],
                                                     [game_setting],
                                                     [cancel_state],
                                                     [cancel_data]], )
    return keyboard


def registered_players_inline_kb(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text="😎 Press for update user lists ", callback_data=f"_update_user_lists_"),
        InlineKeyboardButton(text="🎮 Start game ", callback_data=f"_start_game_pressed_")]

    if kwargs:
        for nickname, annotation in kwargs.items():
            user_id = annotation.get('user_id', 0)
            buttons.append(InlineKeyboardButton(text=f"Player: {nickname}",
                                                callback_data=f"__{nickname}__player__"))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb


def game_process_menu(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text="❌ 🎮 Finish game ", callback_data=f"_finish_game_pressed_")]

    if kwargs:
        for nickname, annotation in kwargs.items():
            user_id = annotation.get('user_id', 0)
            buttons.append(InlineKeyboardButton(text=f"Player: {nickname}",
                                                callback_data=f"__{nickname}__player__"))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb
