from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse
from app.models import *
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pymongo
from pymongo import MongoClient
import urllib
import os

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

class mongo(APIView):
    def get(self, request):
        uri = "mongodb+srv://admin:"+ urllib.parse.quote("Admin@123") + "@longshotai.kd4wkfe.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client.data_db
        client_collection = db['data_collection']
        item_type_collection = db['item_type_collection']
        item_collection = db['item_collection']
        # from config.db import item_collection as collection_name, space_collection, item_type_collection

        spaces = item_collection.find()
        print(spaces)
        # return list_serial(spaces)
        return APIResponse("Mongo", status = 200)

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

