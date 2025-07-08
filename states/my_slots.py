from aiogram.fsm.state import StatesGroup, State


class MySlots(StatesGroup):
    choose_bc = State()
    choose_date = State()
