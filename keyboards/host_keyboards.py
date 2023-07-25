from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import HOST_BUTTONS


def main_menu_inline_kb() -> InlineKeyboardMarkup:
    init_game = InlineKeyboardButton(text=HOST_BUTTONS["Start registration"], callback_data="init_game_pressed")
    game_setting = InlineKeyboardButton(text=HOST_BUTTONS["Game setting"], callback_data="setting_game_pressed")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[init_game],
                                                     [game_setting],
                                                     ], )
    return keyboard


def registered_players_inline_kb() -> InlineKeyboardMarkup:
    update_user_list = InlineKeyboardButton(text=HOST_BUTTONS["Refresh"],
                                            callback_data=f"_update_user_lists_")
    start_game = InlineKeyboardButton(text=HOST_BUTTONS["Start game"],
                                      callback_data=f"_start_game_pressed_")
    view_qr_code = InlineKeyboardButton(text=HOST_BUTTONS["View QR code"],
                                        callback_data=f"_view_qr_code_pressed_")
    select_players = InlineKeyboardButton(text=HOST_BUTTONS["View players"],
                                          callback_data=f"_select_players_pressed_")
    # game_setting = InlineKeyboardButton(text=HOST_BUTTONS["Game setting"],
    #                                     callback_data="_setting_game_pressed_")
    exit_main_menu = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                          callback_data=f"_exit_main_menu_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[update_user_list],
                                                     [start_game],
                                                     [view_qr_code],
                                                     [select_players],
                                                     # [game_setting],
                                                     [exit_main_menu],
                                                     ], )
    return keyboard


def select_players_inline_kb(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    delete_all_button = InlineKeyboardButton(text=HOST_BUTTONS["Delete all"],
                                             callback_data=f"_delete_all_players_pressed_")
    exit_button = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                       callback_data=f"_exit_reg_menu_pressed_")
    if kwargs:
        for user_id, annotation in kwargs.items():
            nickname = annotation.get('nickname', 'nickname')
            buttons.append(InlineKeyboardButton(text=f"{HOST_BUTTONS['Player: ']}{nickname}",
                                                callback_data=f"__{user_id}__player__user_id__"))

    buttons.append(exit_button)
    buttons.append(delete_all_button)
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb


def select_one_player_inline_kb(player: int) -> InlineKeyboardMarkup:
    delete_player = InlineKeyboardButton(text=HOST_BUTTONS["Delete"],
                                         callback_data=f"_delete_player_id_{player}_pressed_")
    exit_to_select_players = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                                  callback_data=f"_exit_select_players_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[delete_player],
                                                     [exit_to_select_players],
                                                     ])
    return keyboard


def hide_qr_inline_kb() -> InlineKeyboardMarkup:
    hide_button = InlineKeyboardButton(text=HOST_BUTTONS["Hide"],
                                       callback_data=f"__hide__qr_code__")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[hide_button]])
    return keyboard


def game_settings_inline_kb() -> InlineKeyboardMarkup:
    toast_time = InlineKeyboardButton(text=HOST_BUTTONS["Toast time"],
                                      callback_data=f"_toast_time_pressed")
    start_lives = InlineKeyboardButton(text=HOST_BUTTONS["Start lives"],
                                       callback_data=f"_change_start_lives_pressed")
    win_lives = InlineKeyboardButton(text=HOST_BUTTONS["Win lives"],
                                     callback_data=f"_change_win_lives_pressed")
    spread_roles = InlineKeyboardButton(text=HOST_BUTTONS["Spread roles"],
                                        callback_data=f"_spread_roles_pressed_")
    count_winners = InlineKeyboardButton(text=HOST_BUTTONS["Count winners"],
                                         callback_data=f"_count_winners_pressed_")
    change_reg_code = InlineKeyboardButton(text=HOST_BUTTONS["QR code data"],
                                           callback_data=f"_update_qr_code_data_pressed_")
    reset_settings = InlineKeyboardButton(text=HOST_BUTTONS["Reset by default settings"],
                                          callback_data=f"_reset_settings_pressed_")
    exit_main_menu = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                          callback_data=f"_exit_main_menu_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[toast_time],
                                                     [start_lives],
                                                     [win_lives],
                                                     [spread_roles],
                                                     [count_winners],
                                                     [change_reg_code],
                                                     [reset_settings],
                                                     [exit_main_menu],
                                                     ])
    return keyboard


def set_toast_time_inline_kb() -> InlineKeyboardMarkup:
    plus_n_sec = InlineKeyboardButton(text=HOST_BUTTONS["Plus n sec"],
                                      callback_data=f"_plus_n_sec_pressed_")
    minus_n_sec = InlineKeyboardButton(text=HOST_BUTTONS["Minus n sec"],
                                       callback_data=f"_minus_n_sec_pressed_")
    exit_settings_menu = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                              callback_data=f"_exit_settings_menu_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[plus_n_sec],
                                                     [minus_n_sec],
                                                     [exit_settings_menu],
                                                     ])
    return keyboard


def set_lives_inline_kb() -> InlineKeyboardMarkup:
    plus_lives = InlineKeyboardButton(text=HOST_BUTTONS["Plus n lives"],
                                      callback_data=f"_plus_lives_pressed_")
    minus_lives = InlineKeyboardButton(text=HOST_BUTTONS["Minus n lives"],
                                       callback_data=f"_minus_lives_pressed_")
    exit_settings_menu = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                              callback_data=f"_exit_settings_menu_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[plus_lives],
                                                     [minus_lives],
                                                     [exit_settings_menu],
                                                     ])
    return keyboard


def count_winners_inline_kb() -> InlineKeyboardMarkup:
    plus_one = InlineKeyboardButton(text=HOST_BUTTONS["Plus one"],
                                    callback_data=f"_plus_one_pressed_")
    minus_one = InlineKeyboardButton(text=HOST_BUTTONS["Minus one"],
                                     callback_data=f"_minus_one_pressed_")
    exit_settings_menu = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                              callback_data=f"_exit_settings_menu_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[plus_one],
                                                     [minus_one],
                                                     [exit_settings_menu],
                                                     ])
    return keyboard


def spread_roles_inline_kb():
    buttons = [
        [
            InlineKeyboardButton(text=HOST_BUTTONS["- wolf"],
                                 callback_data="_minus_spread_wolf_pressed_"),
            InlineKeyboardButton(text=HOST_BUTTONS["+ wolf"],
                                 callback_data="_plus_spread_wolf_pressed_"),
        ],
        [
            InlineKeyboardButton(text=HOST_BUTTONS["- human"],
                                 callback_data="_minus_spread_human_pressed_"),
            InlineKeyboardButton(text=HOST_BUTTONS["+ human"],
                                 callback_data="_plus_spread_human_pressed_"),
        ],
        [
            InlineKeyboardButton(text=HOST_BUTTONS["- werewolf"],
                                 callback_data="_minus_spread_werewolf_pressed_"),
            InlineKeyboardButton(text=HOST_BUTTONS["+ werewolf"],
                                 callback_data="_plus_spread_werewolf_pressed_"),
        ],

        [InlineKeyboardButton(text=HOST_BUTTONS["Confirm this spread"],
                              callback_data="_confirm_spread_setting_pressed_"),
         ],

        [InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                              callback_data="_exit_settings_menu_pressed_"),
         ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def confirm_finish_game_process_inline_kb() -> InlineKeyboardMarkup:
    confirm_finish_button = InlineKeyboardButton(text=HOST_BUTTONS["Confirm finish game process"],
                                                 callback_data="_confirm_finish_game_pressed_")
    return_button = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                         callback_data="_return_game_process_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_finish_button],
                                                     [return_button],
                                                     ])
    return keyboard


def game_process_menu_inline_kb() -> InlineKeyboardMarkup:
    update_button = InlineKeyboardButton(text=HOST_BUTTONS["Update info"],
                                         callback_data=f"_update_host_data_pressed_")
    select_players_button = InlineKeyboardButton(text=HOST_BUTTONS["Up / Down - lives"],
                                                 callback_data=f"_select_players_in_game_pressed_")
    finish_game_button = InlineKeyboardButton(text=HOST_BUTTONS["Finish game"],
                                              callback_data=f"_finish_game_pressed_")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[update_button],
                                                     [select_players_button],
                                                     [finish_game_button],
                                                     ])
    return keyboard


def select_players_in_game_inline_kb(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    return_button = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                         callback_data=f"_return_game_process_pressed_")
    if kwargs:
        for user_id, annotation in kwargs.items():
            nickname = annotation.get('nickname', 'nickname')
            buttons.append(InlineKeyboardButton(text=f"🧑 {nickname}",
                                                callback_data=f"__{user_id}__player__user_id__"))

    buttons.append(return_button)
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()  # return object inline kb


def select_one_player_in_game_inline_kb(player_id: int) -> InlineKeyboardMarkup:
    up_lives_player = InlineKeyboardButton(text=HOST_BUTTONS["Up lives"],
                                           callback_data=f"_up___lives_player_id_{player_id}_pressed_")
    down_lives_player = InlineKeyboardButton(text=HOST_BUTTONS["Down lives"],
                                             callback_data=f"_down_lives_player_id_{player_id}_pressed_")

    exit_to_select_players = InlineKeyboardButton(text=HOST_BUTTONS["Exit"],
                                                  callback_data=f"_exit_select_players_pressed_")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[down_lives_player, up_lives_player],
                                                     [exit_to_select_players],
                                                     ])
    return keyboard
