from aiogram.dispatcher.filters.state import StatesGroup, State


class Notes(StatesGroup):
    add_name = State()
    add_text = State()