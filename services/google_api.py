import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


class GoogleAPI:
    SERVICE_ACCOUNT_FILE = 'onecourseproject.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive']
    TOPICS_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
    KNOWLEDGE_SPREADSHEET_ID = os.getenv("KNOWLEDGE_SPREADSHEET_ID")
    FAQ_SPREADSHEET_ID = os.getenv("FAQ_SPREADSHEET_ID")
    service_drive = None
    service_sheets = None

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service_drive = build('drive', 'v3', credentials=credentials)
        self.service_sheets = build('sheets', 'v4', credentials=credentials)

    async def get_themes(self, chapter):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.TOPICS_SPREADSHEET_ID, range=f"{chapter}!A2:B11").execute()
        values = result.get('values', [])
        print(values)
        return values

    async def get_theme_info(self, chapter, theme):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                    range=f"{chapter}!C{int(theme) + 1}:G{int(theme) + 1}").execute()
        values = result.get('values')
        print(values[0])
        return values[0]

    async def get_checkpoint(self, chapter):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                    range=f"{chapter}!I2:N2").execute()
        values = result.get('values')
        print("get_checkpoint- ", values[0])
        return values[0]

    async def get_knowledge(self, chapter):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.KNOWLEDGE_SPREADSHEET_ID,
                                    range=f"{chapter}!A2:B11").execute()
        values = result.get('values', [])
        print("get_knowledge- ", values)
        return values

    async def get_method_info(self, chapter, method_id):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.KNOWLEDGE_SPREADSHEET_ID,
                                    range=f"{chapter}!B{int(method_id)+1}:C{int(method_id)+1}").execute()
        values = result.get('values', [])
        print("get_method- ", values)
        return values[0]

    async def get_faq(self):
        sheet = self.service_sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.FAQ_SPREADSHEET_ID,
                                    range=f"FAQ!A2:A").execute()
        values = result.get('values', [])
        print("get_FAQ- ", values)
        return values


