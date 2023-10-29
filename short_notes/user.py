import types

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from short_notes import db
from short_notes.states import Notes


async def startup_handler(dp, bot):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        message_text = "Hello\nChoose the button below to add new or show all your notes "
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[InlineKeyboardButton(text='Add note', callback_data='add_note'),
                      (InlineKeyboardButton(text='Show notes', callback_data='show_note'))])

        await message.answer(message_text, reply_markup=keyboard)

    @dp.message_handler(state='*', content_types=types.ContentType.ANY)
    async def states_handler(message: types.Message, state: FSMContext):
        state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
        current_state = await state.get_state()

        if current_state == 'Notes:add_name':
            async with state.proxy() as data:
                data['name'] = message.text
            await message.answer('and now you can send me full text')
            await Notes.add_text.set()

        if current_state == 'Notes:add_text':
            async with state.proxy() as data:
                data['text'] = message.text
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[InlineKeyboardButton(text='Add note', callback_data='add_note'),
                           (InlineKeyboardButton(text='Show notes', callback_data='show_note'))])
            text = 'Your note has been successfully added!'

            await db.add_to_db(message.from_user.id, data['name'], data['text'])
            await message.answer(text=text, reply_markup=keyboard)
            await state.finish()

    @dp.callback_query_handler(state='*')
    async def callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
        if callback_query.data == 'add_note':
            text = 'Write down the name of your note'
            await Notes.add_name.set()

            await callback_query.message.answer(text)

        if callback_query.data == 'show_note':
            all_notes = await db.get_from_db(callback_query.from_user.id)
            if not all_notes:
                await callback_query.message.answer(text='Firstly you have to add your first note')
            else:
                await callback_query.message.answer(text='Here is your notes')
                for note in all_notes:
                    name, text = note.values()
                    await callback_query.message.answer(text=f'{name}\n\n{text}')
