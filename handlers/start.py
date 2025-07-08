from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.common import MAIN_MENU
from utils import escape_md

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Send welcome and show main menu."""
    await message.answer(
        escape_md("Привет! Выберите действие:"),
        reply_markup=MAIN_MENU,
    )
