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
        spreadsheet_id = '1SC39VMsTURb6YfAOefsdUmDX2f9oAHztY_zEnGH6Y2s'
        RANGE = 'Sheet1'
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        # fieldnames = ["name", "phone", "email", "income_per_annum", "savings_per_annum"]
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./gsheet_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Saving the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        try:
            service = build('sheets', 'v4', credentials = creds)
            # Calling the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId = spreadsheet_id, range=RANGE).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            for row in values:
                # print(row)
                if(row[4] > row[3]):
                    message.sms(row[0])
        except HttpError as err:
            print(err)

        return APIResponse("Responses Validated", status = 200)