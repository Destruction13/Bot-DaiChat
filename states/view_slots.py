from aiogram.fsm.state import StatesGroup, State


class ViewSlots(StatesGroup):
    choose_bc = State()
    choose_date = State()
    choose_slot = State()
