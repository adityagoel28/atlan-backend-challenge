import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def push_to_google_sheet(data):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials/gsheet.json", scopes=scopes)
        spreadsheet_id = '1SC39VMsTURb6YfAOefsdUmDX2f9oAHztY_zEnGH6Y2s'
        # Add your service account file
        creds = ServiceAccountCredentials.from_json_keyfile_name('gsheet_credentials.json', scopes)
        # Authorize the clientsheet 
        client = gspread.authorize(creds)

        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1OfvbuAM6f7lTmn_43XNrfi5DV50epF4FNcPpxlhYWt4/edit#gid=0")
        worksheet = sheet.get_worksheet(0) # Get the first sheet of the Spreadsheet
        worksheet.clear()
        values = [[data["form_id"]]]
        values.append(["Question", "Answer"])
        for question in data["questions"]:
            values.append([question["question"]] + question["answers"])
        worksheet.append_rows(values)
        print("gsheet updated")
    except Exception as e:
        print(f"An error occurred while pushing data to Google Sheets: {str(e)}")


from django.core.management.base import BaseCommand

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from faker import Faker

fake = Faker("en_US")
RECORD_COUNT = 100

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet
spreadsheet_id = '1SC39VMsTURb6YfAOefsdUmDX2f9oAHztY_zEnGH6Y2s'
RANGE = 'Sheet1'

def main():
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
        # for row in range(2,4):
        #     num1 = int(sheet.values().get(spreadsheetId = spreadsheet_id, range = f'Sheet1!A{row}').execute().get('values', [])[0][0])
        #     num2 = int(sheet.values().get(spreadsheetId = spreadsheet_id, range = f'Sheet1!B{row}').execute().get('values', [])[0][0])
        #     res = num1 + num2
        #     sheet.values().update(spreadsheetId = spreadsheet_id, range = f'Sheet1!C{row}', valueInputOption = 'USER_ENTERED' , body = {'values':[[res]]}).execute()
        RECORDS = 1
        for row in range(2,101):
            # name = sheet.values().get(spreadsheetId = spreadsheet_id, range = f'Sheet1!A{row}').execute().get('values', [])[0][0]
            name = fake.name()
            phone = fake.phone_number()
            email = fake.email()
            income_per_annum = float(fake.pydecimal(left_digits=5, right_digits=2, positive=True))
            savings_per_annum =  float(fake.pydecimal(left_digits=5, right_digits=2, positive=True))

            sheet.values().update(spreadsheetId = spreadsheet_id, range = f'Sheet1!A{row}', valueInputOption = 'USER_ENTERED' , body = {'values':[[name]]}).execute()
            sheet.values().update(spreadsheetId = spreadsheet_id, range = f'Sheet1!B{row}', valueInputOption = 'USER_ENTERED' , body = {'values':[[phone]]}).execute()
            sheet.values().update(spreadsheetId = spreadsheet_id, range = f'Sheet1!C{row}', valueInputOption = 'USER_ENTERED' , body = {'values':[[email]]}).execute()
            sheet.values().update(spreadsheetId = spreadsheet_id, range = f'Sheet1!D{row}', valueInputOption = 'USER_ENTERED' , body = {'values':[[income_per_annum]]}).execute()
            sheet.values().update(spreadsheetId = spreadsheet_id, range = f'Sheet1!E{row}', valueInputOption = 'USER_ENTERED' , body = {'values':[[savings_per_annum]]}).execute()
            print(RECORDS, "Record Generated")
            RECORDS = RECORDS + 1
        print("Data Generated")
        result = sheet.values().get(spreadsheetId = spreadsheet_id, range=RANGE).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            print(row)
    except HttpError as err:
        print(err)

main()