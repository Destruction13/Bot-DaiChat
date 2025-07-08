import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from handlers import start, add_slot, view_slots, my_slots, delete_slot
from storage.database import init_db


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(add_slot.router)
    dp.include_router(view_slots.router)
    dp.include_router(my_slots.router)
    dp.include_router(delete_slot.router)


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    init_db()
    bot = Bot(token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
