from aiogram.filters.state import StatesGroup, State


# Create class heritable from StateGroup for states our FSM
class FSMAdmin(StatesGroup):
    """Create instances of the State class, sequentially
    listing the possible states it will be in
    bot at different moments of interaction with the admin"""

    game_process = State()
    state_2 = State()
    state_3 = State()


