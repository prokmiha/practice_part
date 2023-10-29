import types

from aiogram import types
from command_handling import db


async def startup_handler(dp, bot):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        message_text = ("Hello\nI am simple bot. I can handle commands /start, /help and /history\n"
                        "Now you can text me anything")

        await message.answer(message_text)

    @dp.message_handler(commands=['help'])
    async def help_command(message: types.Message):
        await message.answer('This is "help" command')

    @dp.message_handler(commands=['history'])
    async def help_command(message: types.Message):
        text = ''
        messages = await db.get_from_db(message.from_user.id)
        for history in messages[::-1]:
            text += history + '\n'
        await message.answer(text=text)

    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def echo(message: types.Message):
        message_text = message.text

        await db.add_to_db(message.from_user.id, message_text)
