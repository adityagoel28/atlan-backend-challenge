from twilio.rest import Client
import os
from decouple import config

def sms(data):
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    twilio_number = config('TWILIO_NUMBER')
    client = Client(account_sid, auth_token)

    try:
        response = "Sending SMS"
        # message = client.messages.create(body=f"{data}'s savings is greater than income", from_ = twilio_number, to='+918887874339')
        # print(message.sid)
        # response = message.sid
    except Exception as e:
        print(f"An error occurred while sending the SMS: {str(e)}")
        response = e
    return response
