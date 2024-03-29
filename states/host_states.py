from aiogram.filters.state import StatesGroup, State


# Create class heritable from StateGroup for states our FSM
class FSMHost(StatesGroup):
    """Create instances of the State class, sequentially
    listing the possible states it will be in
    bot at different moments of interaction with the admin"""

    input_room_name = State()
    input_password = State()
    wait_register_players = State()
    game_process = State()
    game_setting_process = State()

