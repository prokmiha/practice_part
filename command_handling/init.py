import asyncio
from configparser import ConfigParser

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from command_handling.user import startup_handler
import db


async def start():
    await db.start_db()
    config = ConfigParser()
    config.read(filenames='config.ini')
    token = config.get('BOT_TOKEN', 'token').replace('\\n', '\n')
    bot = Bot(token=token)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    await asyncio.gather(dp.start_polling(), startup_handler(dp, bot))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
