from aiogram.fsm.state import StatesGroup, State


class DeleteSlot(StatesGroup):
    choose_bc = State()
    choose_date = State()
    choose_slot = State()
