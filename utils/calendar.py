from aiogram_calendar import SimpleCalendar


RU_DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
RU_MONTHS = [
    "Янв",
    "Фев",
    "Мар",
    "Апр",
    "Май",
    "Июн",
    "Июл",
    "Авг",
    "Сен",
    "Окт",
    "Ноя",
    "Дек",
]


def get_ru_calendar() -> SimpleCalendar:
    cal = SimpleCalendar()
    cal._labels.days_of_week = RU_DAYS
    cal._labels.months = RU_MONTHS
    cal._labels.cancel_caption = "Отмена"
    cal._labels.today_caption = "Сегодня"
    return cal
