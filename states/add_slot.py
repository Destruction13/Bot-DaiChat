from aiogram.fsm.state import StatesGroup, State


class AddSlot(StatesGroup):
    choose_bc = State()
    choose_date = State()
    enter_time = State()
    enter_link = State()
