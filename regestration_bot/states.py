from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    name_waiting = State()
    surname_waiting = State()
    email_waiting = State()
    phone_waiting = State()