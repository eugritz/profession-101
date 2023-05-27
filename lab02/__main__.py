import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from common import router as common_router
from search import router as  search_router

async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    bot = Bot(os.getenv('API_TOKEN') or '')
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(common_router)
    dp.include_router(search_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
