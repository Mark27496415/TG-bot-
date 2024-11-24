from pyrogram.types import KeyboardButton, InlineKeyboardButton

from pyrogram import emoji

# Общие кнопки
back_button = KeyboardButton(f"{emoji.BACK_ARROW} Назад")
# Кнопки главного меню
time_button = KeyboardButton(f"{emoji.ALARM_CLOCK} Время")
help_button = KeyboardButton(f"{emoji.WHITE_QUESTION_MARK} Помощь")
weather_button = KeyboardButton(f"{emoji.SUN} Погода")

change_city_button = KeyboardButton(f"{emoji.TOKYO_TOWER} Установить город")

weather_current_inline_button = InlineKeyboardButton(f"{emoji.FIVE_O_CLOCK} Погода сейчас", "weather_current")
weather_forecast_inline_button = InlineKeyboardButton(f"{emoji.CALENDAR} Прогноз погоды", "weather_forecast")
