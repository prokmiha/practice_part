from io import BytesIO

import aiohttp
import qrcode
import json
import asyncio


class ApiKey:
	_instances = {}

	def __new__(cls, api_key):
		if api_key not in cls._instances:
			cls._instances[api_key] = super(ApiKey, cls).__new__(cls)
		return cls._instances[api_key]

	def __init__(self, api_key):
		self.api_key = api_key

	def get_api_key(self):
		return self.api_key

	def set_api_key(self, api_key):
		self.api_key = api_key


class NowPayments:
	def __init__(self, api_key: str):
		self.__api_key = api_key
		self.url = "https://api.nowpayments.io/v1/payment"

	async def create_payment(self, amount: int, order_id: str = None, order_description: str = None) -> dict:
		headers = {
			'x-api-key': self.__api_key,
			'Content-Type': 'application/json'
		}
		payload = {
			"price_amount": amount,
			"price_currency": "usd",
			"pay_currency": "trx",
			"ipn_callback_url": "https://nowpayments.io",
		}
		if order_id is not None:
			payload['order_id'] = order_id

		if order_description is not None:
			payload['order_description'] = order_description
		payloads = json.dumps(payload)

		async with aiohttp.ClientSession() as session:
			async with session.request("POST", self.url, headers=headers, data=payloads) as request:
				response_json = await request.json()
				if response_json.get('payment_status') == 'waiting':
					data = {
						'payment_id': response_json["payment_id"],
						'pay_address': response_json["pay_address"],
						'pay_amount': response_json['pay_amount'],
					}

					payment_data = f"tron:{data['pay_address']}?amount={data['pay_amount']}"
					qr = qrcode.QRCode(
						version=1,
						error_correction=qrcode.constants.ERROR_CORRECT_L,
						box_size=10,
						border=4,
					)

					qr.add_data(payment_data)
					qr.make(fit=True)
					img = qr.make_image(fill_color="black", back_color="white")

					buffer = BytesIO()
					img.save(buffer)

					telegram_upload_url = "https://telegra.ph/upload"
					data_buffer = aiohttp.FormData()
					data_buffer.add_field('file', buffer.getvalue(), filename='temp_qr.png', content_type='image/png')

					async with aiohttp.ClientSession() as telegram_session:
						async with telegram_session.post(telegram_upload_url, data=data_buffer, ssl=False) as telegram_response:
							if telegram_response.status == 200:
								result = await telegram_response.json()
								if "src" in result[0]:
									qr_url = "https://telegra.ph" + result[0]["src"]
									data['qr_url'] = qr_url
					return data

	async def payment_status(self, payment_id: str):
		url = f"{self.url}/{payment_id}"
		headers = {
			'x-api-key': self.__api_key,
		}
		payment_statuses = 'waiting'
		async with aiohttp.ClientSession() as session:
			while payment_statuses == 'waiting':
				async with session.get(url, headers=headers) as response:
					response_json = await response.json()
					payment_statuses = response_json.get('payment_status')
					await asyncio.sleep(15) if payment_statuses == 'waiting' else lambda: payment_statuses


if __name__ == "__main__":
	api_manager = ApiKey("78TAR73-V8HMA8A-PRFFKDW-C40SBWQ")
	api_key = api_manager.get_api_key()
	payment = NowPayments(api_key)
	loop = asyncio.get_event_loop()
	result = loop.run_until_complete(payment.create_payment(100))
	result = loop.run_until_complete(payment.payment_status(result['payment_id']))

	loop.close()
