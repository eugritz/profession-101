import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from Common import register_handlers

async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    bot = Bot(os.getenv('API_TOKEN') or '')
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers(dp)

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
