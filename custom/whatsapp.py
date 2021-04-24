import os
from twilio.rest import Client
from custom.credentials import token, account


def whatsapp_message(token, account, to_number, message):
	client = Client(account, token)
	from_number = 'whatsapp:+14155238886'
	to_number = 'whatsapp:'+to_number
	client.messages.create(body=message, from_ = from_number, to= to_number)