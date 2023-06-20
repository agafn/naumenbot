import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from request_processing import process_rasa_request, run_rasa_server
import asyncio

import os

# Настройки бота
BOT_TOKEN = os.getenv('TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.KeyboardButton('Open', web_app=WebAppInfo(url='https://naumenbot.tpu.ru/register_user.html')))
    await message.answer("Привет! Для использования бота пройдите, пожалуйста, авторизацию.",reply_markup=markup)
    await message.delete()


# Обработчик команды /login
@dp.message_handler(commands=['login'])
async def send_welcome(message: types.Message):
    await message.answer("Авторизация успешно пройдена. Что хотели бы спросить?")
    await message.delete()


# Обработчик всех текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    user_message = message.text

    # Обрабатываем запрос к серверу Rasa
    bot_response = process_rasa_request(user_message)

    await message.reply(bot_response)


async def main():
    # Запуск сервера Rasa в асинхронном режиме
    rasa_task = asyncio.create_task(run_rasa_server())

    # Запуск бота Telegram
    try:
        await dp.start_polling()
        print("Бот запущен.")
    except Exception as e:
        print(f"Произошла ошибка при запуске бота: {e}")

    #await rasa_task


# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    print("Сервер и Бот успешно запущены.")
