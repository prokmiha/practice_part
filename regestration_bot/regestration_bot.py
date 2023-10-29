import types

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states import Registration


async def startup_handler(dp, bot):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        message_text = "Hello\nLet's start registration"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='Register', callback_data='reg_start'))

        await message.answer(message_text, reply_markup=keyboard)

    @dp.message_handler(state='*', content_types=types.ContentType.ANY)
    async def states_handler(message: types.Message):
        state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
        current_state = await state.get_state()

        if current_state == 'Registration:name_waiting':
            async with state.proxy() as data:
                data['name'] = message.text
            await message.answer('Now tell me your surname')
            await Registration.surname_waiting.set()

        if current_state == 'Registration:surname_waiting':
            async with state.proxy() as data:
                data['surname'] = message.text
            await message.answer('Please, tell me you Email address')
            await Registration.email_waiting.set()

        if current_state == 'Registration:email_waiting':
            async with state.proxy() as data:
                data['email'] = message.text
            await message.answer('And the last one is your phone number')
            await Registration.phone_waiting.set()

        if current_state == 'Registration:phone_waiting':
            async with state.proxy() as data:
                data['phone'] = message.text
            await message.answer(
                f"Here is the result:\nName: {data['name']}\nSurname: {data['surname']}\nEmail: {data['email']}\nPhone: {data['phone']}")
            await state.finish()

    @dp.callback_query_handler(state='*')
    async def callback_handler(callback_query: types.CallbackQuery):
        if callback_query.data == 'reg_start':
            text = 'Tell me your name'
            await Registration.name_waiting.set()

            await callback_query.message.edit_text(text)
