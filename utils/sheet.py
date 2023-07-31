import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv
import boto3
from decouple import config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet
spreadsheet_id = '1SC39VMsTURb6YfAOefsdUmDX2f9oAHztY_zEnGH6Y2s'
RANGE = 'Sheet1'

def push_to_google_sheet(data):
    service = authorise()
    # adding a record at the end of the sheet
    values = [
        [
            data['client_name'],
            data['client_email'],
            data['income_per_annum'],
            data['savings_per_annum'],
            data['mobile_number'],
        ],
            # Additional rows ...
    ]
    body = {"values": values}
    result = (
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=RANGE, valueInputOption="USER_ENTERED", body=body,
        )
        .execute()
    )
    print("{0} cells appended in the sheet.".format(result.get("updates").get("updatedCells")))

def authorise():
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
        # Call the Sheets API
        sheet = service.spreadsheets()
        return service
        
    except HttpError as err:
        print(err)

authorise()

def push_to_s3():
    service = authorise()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = spreadsheet_id, range=RANGE).execute()
    values = result.get('values', [])

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(values)

    aws_access_key_id = config('aws_access_key_id')
    aws_secret_access_key = config('aws_secret_access_key')

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    filename = 'data.csv'
    bucket_name = 'atlan-data-collection'

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(filename, bucket_name, filename)