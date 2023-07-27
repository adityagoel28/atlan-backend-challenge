from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse
from app.models import *

from twilio.rest import Client
import os

# Create your views here.
def home(request):
    return APIResponse("Home", status=200)

class HealthCheck(APIView):
    def get(self, request):
        return APIResponse("Health OK", status=200)

def sms(request):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    twilio_number = os.environ['TWILIO_NUMBER']

    try:
        message = client.messages.create(body='Hi', from_ = twilio_number, to='+918887874339')
        print(message.sid)
    except Exception as e:
        print(f"An error occurred while sending the SMS: {str(e)}")
    return APIResponse("SMS", status=200)