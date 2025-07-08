import re
from urllib.parse import urlparse

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendarCallback

from keyboards.common import business_centers_kb, MAIN_MENU
from states.add_slot import AddSlot
from storage.database import add_slot
from utils.calendar import get_ru_calendar

router = Router()

TIME_PATTERN = re.compile(r"^\d{2}:\d{2}\s*-\s*\d{2}:\d{2}$")


@router.message(F.text == "Разместить слот")
async def start_add(message: Message, state: FSMContext) -> None:
    await state.set_state(AddSlot.choose_bc)
    await message.answer(
        "Выберите бизнес-центр:",
        reply_markup=business_centers_kb("addbc"),
    )


@router.callback_query(F.data.startswith("addbc:"), AddSlot.choose_bc)
async def bc_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    bc = callback.data.split(":", 1)[1]
    await state.update_data(bc=bc)
    cal = get_ru_calendar()
    markup = await cal.start_calendar()
    await callback.message.edit_text("Выберите дату:", reply_markup=markup)
    await callback.answer()
    await state.set_state(AddSlot.choose_date)


@router.callback_query(AddSlot.choose_date, SimpleCalendarCallback.filter())
async def date_chosen(
    callback: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext
) -> None:
    cal = get_ru_calendar()
    selected, date = await cal.process_selection(callback, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%Y-%m-%d"))
        await callback.message.answer(
            "Введите время слота в формате ЧЧ:ММ - ЧЧ:ММ"
        )
        await state.set_state(AddSlot.enter_time)
    # calendar already edited by library


@router.message(AddSlot.enter_time)
async def time_entered(message: Message, state: FSMContext) -> None:
    if not TIME_PATTERN.match(message.text):
        await message.answer(
            "Неверный формат времени. Используйте ЧЧ:ММ - ЧЧ:ММ"
        )
        return
    start, end = [t.strip() for t in message.text.split("-")]
    try:
        int(start[:2]), int(start[3:])
        int(end[:2]), int(end[3:])
    except ValueError:
        await message.answer("Некорректное время")
        return
    await state.update_data(time=f"{start} - {end}")
    await state.set_state(AddSlot.enter_link)
    await message.answer("Введите ссылку на встречу")


@router.message(AddSlot.enter_link)
async def link_entered(message: Message, state: FSMContext) -> None:
    link = message.text.strip()
    parsed = urlparse(link)
    if not parsed.scheme.startswith("http"):
        await message.answer("Некорректная ссылка")
        return
    data = await state.get_data()
    success = add_slot(
        message.from_user.id,
        data["bc"],
        data["date"],
        data["time"],
        link,
    )
    if success:
        await message.answer("Слот успешно добавлен", reply_markup=MAIN_MENU)
    else:
        await message.answer("Такой слот уже существует", reply_markup=MAIN_MENU)
    await state.clear()
