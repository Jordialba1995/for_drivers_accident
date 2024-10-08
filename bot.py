import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters.command import Command

import steps
from config_reader import config
# импортируем файлы из каталога handlers/ и подключаем роутеры из этих файлов к диспетчеру. И здесь снова важен порядок импортов!
# from handlers import questions, different_types


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.bot_token.get_secret_value())

# Диспетчер
dp = Dispatcher()

# регистрация роутеров
dp.include_routers(steps.router)



# @dp.message(Command('start'))
# async def cmd_start(message: types.Message):
#     await message.answer('Hello')

















if __name__ == '__main__':
    asyncio.run(main())