import time
import operator

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery,ForceReply

import config
import buttons
import keyboards
from custom_filters import button_filter, inline_button_filter, reply_text_filter
from weather import get_current_weather, get_forecast

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="RobotVerter",  # можно указать любое имя
)


@bot.on_message(filters=filters.command("calc"))
async def calc_command(client: Client, message: Message):
    ops = {
        "+": operator.add, "-": operator.sub,
        "*": operator.mul, "/": operator.truediv,
    }
    if len(message.command) != 4:
        return await message.reply(
            "Неверное количество аргументов\n"
            "Пример использования:\n"
            "/calc 1 + 2\n"
        )
    _, left, op, right = message.command
    op = ops.get(op)
    if op is None:
        return await message.reply("Неизвестный оператор")
    if not left.isdigit() or not right.isdigit():
        return await message.reply("Аргументы должны быть числами")
    left, right = int(left), int(right)
    await message.reply(f"Результат: {op(left, right)}")


@bot.on_message(filters=filters.command("time") | button_filter(buttons.time_button))
async def time_command(client: Client, message: Message):
    current_time = time.strftime("%H:%M:%S")
    await message.reply(f"Текущее время: {current_time}")


@bot.on_message(filters=filters.command("start") | button_filter(buttons.back_button))
async def echo(client: Client, message: Message):
    await message.reply(
        "Привет! Я бот, который умеет считать и показывать время.\n"
        f"Нажми на кнопку {buttons.help_button.text} для получения списка команд.",
        reply_markup=keyboards.main_keyboard
    )


@bot.on_message(filters=filters.command('help') | button_filter(buttons.help_button))
async def help_command(bot: Client, message: Message):
    commands = await bot.get_bot_commands()
    text_commands = "Список доступных команд:\n\n"
    for command in commands:
        text_commands += f"/{command.command} - {command.description}\n"
    await message.reply(text_commands)


change_city_text = f"Меняем город!\n\nНапиши в ответ на это сообщение название своего города, а я его запомню!"

@bot.on_message(filters=filters.command("change_city") | button_filter(buttons.change_city_button))
async def change_city_command(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=change_city_text,
        reply_markup=ForceReply(True),
    )

@bot.on_message(filters=filters.reply & reply_text_filter(change_city_text))
async def change_city_reply(client: Client, message: Message):
    global city
    city = message.text
    await message.reply(
    "Город успешно изменён!",
        reply_markup=keyboards.main_keyboard,
    )


@bot.on_message(filters=filters.command("weather") | button_filter(buttons.weather_button))
async def weather_command(client: Client, message: Message):
    await message.reply("Установи свой город \n\n Ты можешь изменить свой текущий город чтобы узнать погоду у себя ")
    weather = get_current_weather(city)
    await message.reply(
        weather,
        reply_markup=keyboards.weather_inline_keyboard
    )


@bot.on_callback_query(filters=inline_button_filter(buttons.weather_current_inline_button))
async def weather_current_inline_button_callback(client: Client, query: CallbackQuery):

    weather = get_current_weather(city)
    if weather == query.message.text:
        return
    await query.message.edit_text(
        weather,
        reply_markup=keyboards.weather_inline_keyboard
)


@bot.on_callback_query(filters=inline_button_filter(buttons.weather_forecast_inline_button))
async def weather_forecast_inline_button_callback(client: Client, query: CallbackQuery):

    weather = get_forecast(city)
    if weather == query.message.text:
        return

    await query.message.edit_text(
        weather,
        reply_markup=keyboards.weather_inline_keyboard
)



bot.run()
