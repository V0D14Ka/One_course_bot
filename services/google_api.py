import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


class GoogleAPI:
    SERVICE_ACCOUNT_FILE = 'onecourseproject.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive']
    SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
    service_drive = None
    service_sheets = None

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service_drive = build('drive', 'v3', credentials=credentials)
        self.service_sheets = build('sheets', 'v4', credentials=credentials)

    async def get_themes(self, chapter):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=f"{chapter}!A1:B10").execute()
        values = result.get('values', [])
        print(values)
        return values

    async def get_theme_info(self, chapter, theme):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                    range=f"{chapter}!C{theme}:G{theme}").execute()
        values = result.get('values')
        print(values[0])
        return values[0]
