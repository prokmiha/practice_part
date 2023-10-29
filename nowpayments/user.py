import types

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from nowpayments.request_nowpayments import NowPayments, ApiKey


async def startup_handler(dp, bot):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        message_text = "Hello\nLet's start registration"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='Buy option one (5$)', callback_data='payment_5'),
                     InlineKeyboardButton(text='Buy option one (10$)', callback_data='payment_10'))

        await message.answer(message_text, reply_markup=keyboard)

    @dp.callback_query_handler(state='*')
    async def callback_handler(callback_query: types.CallbackQuery):
        api_manager = ApiKey("78TAR73-V8HMA8A-PRFFKDW-C40SBWQ")
        api_key = api_manager.get_api_key()
        request_payment_details = NowPayments(api_key=api_key)

        if callback_query.data.startswith('payment_'):
            _, price = callback_query.data.split('_')

            payment_details = await request_payment_details.create_payment(price)

            text = (
                f'Your payment ID: {payment_details["payment_id"]}\nPayment address: {payment_details["pay_address"]}\n'
                f'Final price in TRX: {payment_details["pay_amount"]}\nQR Code: {payment_details["qr_url"]}')
            button_text = 'Check status'

            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton(text=button_text, callback_data=f'status_{payment_details["payment_id"]}'))

            await callback_query.message.answer(text=text, reply_markup=keyboard)

        if callback_query.data.startswith("status_"):
            _, id = callback_query.data.split('_')

            await callback_query.message.answer(text='We will inform you, when your transaction status will be updated')

            status_check = await request_payment_details.payment_status(payment_id=id)
            text = f'Your payment was marked as: {status_check}'

            await callback_query.message.answer(text=text)
