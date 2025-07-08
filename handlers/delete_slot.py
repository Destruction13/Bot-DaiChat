from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendarCallback

from keyboards.common import business_centers_kb, slots_kb, MAIN_MENU
from states.delete_slot import DeleteSlot
from storage.database import get_user_slots, remove_slot
from utils.calendar import get_ru_calendar

router = Router()


@router.message(F.text == "Удалить слот")
async def start_delete(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteSlot.choose_bc)
    await message.answer("Выберите бизнес-центр:", reply_markup=business_centers_kb("delbc"))


@router.callback_query(DeleteSlot.choose_bc, F.data.startswith("delbc:"))
async def del_bc_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    bc = callback.data.split(":", 1)[1]
    await state.update_data(bc=bc)
    cal = get_ru_calendar()
    markup = await cal.start_calendar()
    await callback.message.edit_text("Выберите дату:", reply_markup=markup)
    await callback.answer()
    await state.set_state(DeleteSlot.choose_date)


@router.callback_query(DeleteSlot.choose_date, SimpleCalendarCallback.filter())
async def del_date_chosen(
    callback: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext
) -> None:
    cal = get_ru_calendar()
    selected, date = await cal.process_selection(callback, callback_data)
    if selected:
        date_str = date.strftime("%Y-%m-%d")
        data = await state.get_data()
        bc = data["bc"]
        slots = get_user_slots(callback.from_user.id, bc, date_str)
        if not slots:
            await callback.message.answer("Слотов нет", reply_markup=MAIN_MENU)
            await state.clear()
            return
        await state.update_data(date=date_str)
        times = [s[0] for s in slots]
        await callback.message.answer(
            "Выберите слот для удаления:", reply_markup=slots_kb("deltime", times)
        )
        await state.set_state(DeleteSlot.choose_slot)


@router.callback_query(DeleteSlot.choose_slot, F.data.startswith("deltime:"))
async def slot_delete(callback: CallbackQuery, state: FSMContext) -> None:
    time = callback.data.split(":", 1)[1]
    data = await state.get_data()
    remove_slot(data["bc"], data["date"], time)
    await callback.message.edit_text("Слот удален", reply_markup=MAIN_MENU)
    await state.clear()
    await callback.answer()
