from setuptools import setup

setup(
	name="nowpayments_request",
	version="0.1",
	author="AIMA",
	description="Generate and check payment status",
	install_requires=[

		"aiohttp==3.8.6",
		"aiosignal==1.3.1",
		"async-timeout==4.0.3",
		"attrs==23.1.0",
		"charset-normalizer==3.3.0",
		"colorama==0.4.6",
		"frozenlist==1.4.0",
		"idna==3.4",
		"multidict==6.0.4",
		"Pillow==10.0.1",
		"pypng==0.20220715.0",
		"qrcode==7.4.2",
		"typing_extensions==4.8.0",
		"yarl==1.9.2",
	],
)