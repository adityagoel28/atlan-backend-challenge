from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse
from app.models import *

from utils import message
from utils import sheet
from app.models import *
from decouple import config
from twilio.rest import Client

# Create your views here.
def home(request):
    return APIResponse("Home", status = 200)

class HealthCheck(APIView):
    def get(self, request):
        message.sms('a')
        return APIResponse("Health OK", status = 200)

class validateResponses(APIView):
    def get(self, request):
        sheet.push_to_s3()
        return APIResponse("Responses Validated", status = 200)


class clientData(APIView):
    def post(self, request):
        client_name = request.data.get("name")
        client_email = request.data.get("email")
        income_per_annum = request.data.get("income_per_annum")
        savings_per_annum = request.data.get("savings_per_annum")
        mobile_number = request.data.get("phone")
        data = {'client_name': client_name, 'client_email': client_email, 'income_per_annum': income_per_annum, 'savings_per_annum': savings_per_annum, 'mobile_number': mobile_number}
        if Clients.objects.filter(client_email = client_email).exists():
            return APIResponse("Client already exists", status = 400)
        else:
            Clients.objects.create(client_email = client_email, client_name = client_name,
                                   income_per_annum = income_per_annum, savings_per_annum = savings_per_annum, mobile_number = mobile_number).save()
            
            account_sid = config('TWILIO_ACCOUNT_SID')
            auth_token = config('TWILIO_AUTH_TOKEN')
            twilio_number = config('TWILIO_NUMBER')
            client = Client(account_sid, auth_token)

            try:
                sheet.push_to_google_sheet(data)
                message = client.messages.create(body=f"Hi {client_name}, thanks for your response. Please find your details - Email: {client_email}, Mobile Number: {mobile_number}, Income per Annum: {income_per_annum}, Savings per annum: {savings_per_annum} ", from_ = twilio_number, to='+918887874339')
            except Exception as e:
                print(f"An error occurred while sending the SMS: {str(e)}")
        return APIResponse("Client created", status = 200)

