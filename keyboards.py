from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
import buttons

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.time_button, buttons.help_button],
        [buttons.change_city_button],
        [buttons.weather_button]
    ],
    resize_keyboard=True,
    )


weather_inline_keyboard = InlineKeyboardMarkup(
    [
        [buttons.weather_current_inline_button],
        [buttons.weather_forecast_inline_button],
    ],
)
