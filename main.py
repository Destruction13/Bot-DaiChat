import asyncio
import os


BOT_TOKEN = "7845798275:AAG0OOzduEZste-tdt3WcUEkFw_LdXFpbHQ"


def load_dotenv(path: str = ".env") -> None:
    """Load environment variables from a simple .env file."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            if line.startswith("#") or "=" not in line:
                continue
            key, value = line.strip().split("=", 1)
            os.environ.setdefault(key, value)

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import start, add_slot, view_slots, my_slots, delete_slot
from storage.database import init_db


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(add_slot.router)
    dp.include_router(view_slots.router)
    dp.include_router(my_slots.router)
    dp.include_router(delete_slot.router)


async def main() -> None:
    load_dotenv()
    token = BOT_TOKEN

    init_db()
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()
    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
