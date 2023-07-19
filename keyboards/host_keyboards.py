from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder


from lexicon.lexicon import HOST_BOTTOMS


def host_inline_kb() -> InlineKeyboardMarkup:
    init_game = InlineKeyboardButton(text=HOST_BOTTOMS["Start registration in game"], callback_data="init_game_pressed")
    room_name = InlineKeyboardButton(text=HOST_BOTTOMS["Change room name"], callback_data="change_room_name_pressed")
    change_pass = InlineKeyboardButton(text=HOST_BOTTOMS["Change password"], callback_data="change_pass_pressed")
    game_setting = InlineKeyboardButton(text=HOST_BOTTOMS["Game setting"], callback_data="setting_game_pressed")
    cancel_state = InlineKeyboardButton(text=HOST_BOTTOMS["Cancel state"], callback_data="cancel_state")
    cancel_data = InlineKeyboardButton(text=HOST_BOTTOMS["Cancel data"], callback_data="_cancel_all_data_")

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
        InlineKeyboardButton(text=HOST_BOTTOMS["Press for update user lists"], callback_data=f"_update_user_lists_"),
        InlineKeyboardButton(text=HOST_BOTTOMS["Start game"], callback_data=f"_start_game_pressed_"),
        InlineKeyboardButton(text=HOST_BOTTOMS["Exit to the main menu"], callback_data=f"_exit_main_menu_pressed_")]

    if kwargs:
        for user_id, annotation in kwargs.items():
            nickname = annotation.get('nickname', 'nickname')
            buttons.append(InlineKeyboardButton(text=f"{HOST_BOTTOMS['Player: ']}{nickname}",
                                                callback_data=f"__{user_id}__player__user_id__"))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb


def game_process_menu(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text=HOST_BOTTOMS["Finish game"], callback_data=f"_finish_game_pressed_")]

    if kwargs:
        for user_id, annotation in kwargs.items():
            nickname = annotation.get('nickname', 'nickname')
            buttons.append(InlineKeyboardButton(text=f"{HOST_BOTTOMS['Player: ']}{nickname}",
                                                callback_data=f"__{user_id}__player__user_id__"))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb
