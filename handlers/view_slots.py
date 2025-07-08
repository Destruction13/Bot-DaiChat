from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendarCallback

from keyboards.common import business_centers_kb, slots_kb, slot_actions_kb, MAIN_MENU
from states.view_slots import ViewSlots
from storage.database import get_slots, remove_slot
from utils.calendar import get_ru_calendar
from utils import escape_md

router = Router()


@router.message(F.text == "Доступные слоты")
async def start_view(message: Message, state: FSMContext) -> None:
    await state.set_state(ViewSlots.choose_bc)
    await message.answer(
        escape_md("Выберите бизнес-центр:"),
        reply_markup=business_centers_kb("viewbc"),
    )


@router.callback_query(F.data.startswith("viewbc:"), ViewSlots.choose_bc)
async def view_bc_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    bc = callback.data.split(":", 1)[1]
    await state.update_data(bc=bc)
    cal = get_ru_calendar()
    markup = await cal.start_calendar()
    await callback.message.edit_text(
        escape_md("Выберите дату:"), reply_markup=markup
    )
    await callback.answer()
    await state.set_state(ViewSlots.choose_date)


@router.callback_query(ViewSlots.choose_date, SimpleCalendarCallback.filter())
async def view_date_chosen(
    callback: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext
) -> None:
    cal = get_ru_calendar()
    selected, date = await cal.process_selection(callback, callback_data)
    if selected:
        date_str = date.strftime("%Y-%m-%d")
        data = await state.get_data()
        bc = data["bc"]
        slots = get_slots(bc, date_str)
        if not slots:
            await callback.message.answer(
                escape_md("На этот день нет доступных слотов"),
                reply_markup=MAIN_MENU,
            )
            await state.clear()
            return
        times = [s[1] for s in slots]
        await state.update_data(date=date_str, slots={s[1]: s[2] for s in slots})
        await callback.message.answer(
            escape_md("Доступные слоты:"),
            reply_markup=slots_kb("viewtime", times),
        )
        await state.set_state(ViewSlots.choose_slot)


@router.callback_query(ViewSlots.choose_slot, F.data.startswith("viewtime:"))
async def slot_selected(callback: CallbackQuery, state: FSMContext) -> None:
    time = callback.data.split(":", 1)[1]
    data = await state.get_data()
    link = data["slots"][time]
    bc = data["bc"]
    date = data["date"]
    await callback.message.edit_text(
        escape_md(f"Слот {time}\nСсылка: {link}"),
        reply_markup=slot_actions_kb(bc, date, time),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("take:"))
async def take_slot(callback: CallbackQuery) -> None:
    _, bc, date, time = callback.data.split(":", 3)
    remove_slot(bc, date, time)
    await callback.message.edit_text(escape_md("Слот забран"))
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.clear()
    await callback.answer()
