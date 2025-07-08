from aiogram import Router
from aiogram.types import Message

from keyboards.common import MAIN_MENU

router = Router()


@router.message(commands=["start"])
async def cmd_start(message: Message) -> None:
    """Send welcome and show main menu."""
    await message.answer(
        "Привет! Выберите действие:", reply_markup=MAIN_MENU
    )
