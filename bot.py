import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage


import steps
from config_reader import config


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





if __name__ == '__main__':
    asyncio.run(main())