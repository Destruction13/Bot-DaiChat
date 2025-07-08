from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Разместить слот")],
        [KeyboardButton(text="Доступные слоты")],
        [KeyboardButton(text="Мои слоты")],
        [KeyboardButton(text="Удалить слот")],
    ],
    resize_keyboard=True,
)

BUSINESS_CENTERS = [
    "Морозов",
    "Строганов",
    "Аврора",
    "Мамонтов",
    "Нева",
    "Бенуа",
    "Феррум",
    "Скайлайн",
    "Палладиум",
    "RubinPlaza",
]


def business_centers_kb(prefix: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=bc, callback_data=f"{prefix}:{bc}")]
        for bc in BUSINESS_CENTERS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def slots_kb(prefix: str, slots: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=s, callback_data=f"{prefix}:{s}")]
        for s in slots
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def slot_actions_kb(bc: str, date: str, time: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Забрать",
                    callback_data=f"take:{bc}:{date}:{time}",
                ),
                InlineKeyboardButton(text="Отмена", callback_data="cancel"),
            ]
        ]
    )
