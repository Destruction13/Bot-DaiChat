from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendarCallback

from keyboards.common import business_centers_kb, MAIN_MENU
from states.my_slots import MySlots
from storage.database import get_user_slots
from utils.calendar import get_ru_calendar
from utils import escape_md

router = Router()


@router.message(F.text == "Мои слоты")
async def start_my_slots(message: Message, state: FSMContext) -> None:
    await state.set_state(MySlots.choose_bc)
    await message.answer(
        escape_md("Выберите бизнес-центр:"),
        reply_markup=business_centers_kb("mybc"),
    )


@router.callback_query(MySlots.choose_bc, F.data.startswith("mybc:"))
async def my_bc_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    bc = callback.data.split(":", 1)[1]
    await state.update_data(bc=bc)
    cal = get_ru_calendar()
    markup = await cal.start_calendar()
    await callback.message.edit_text(
        escape_md("Выберите дату:"), reply_markup=markup
    )
    await callback.answer()
    await state.set_state(MySlots.choose_date)


@router.callback_query(MySlots.choose_date, SimpleCalendarCallback.filter())
async def my_date_chosen(
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
            await callback.message.answer(
                escape_md("У вас нет слотов на эту дату"),
                reply_markup=MAIN_MENU,
            )
        else:
            text = "\n".join(
                escape_md(f"{t} — {link}") for t, link in slots
            )
            await callback.message.answer(text, reply_markup=MAIN_MENU)
        await state.clear()
