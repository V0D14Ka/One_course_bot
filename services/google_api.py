import os
import datetime as dt
import asyncio
import json
from dotenv import load_dotenv
from aiogoogle import Aiogoogle
from googleapiclient.errors import HttpError

load_dotenv()


def load_creds_from_file(file_path):
    with open(file_path) as f:
        creds_data = json.load(f)
    return creds_data


class GoogleAPI:
    SERVICE_ACCOUNT_FILE = 'onecourseproject.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/calendar']
    TOPICS_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
    KNOWLEDGE_SPREADSHEET_ID = os.getenv("KNOWLEDGE_SPREADSHEET_ID")
    DAY_TASK_SPREADSHEET_ID = os.getenv("DAY_TASK_SPREADSHEET_ID")
    FAQ_SPREADSHEET_ID = os.getenv("FAQ_SPREADSHEET_ID")

    async def init(self):
        creds_data = load_creds_from_file(self.SERVICE_ACCOUNT_FILE)
        async with Aiogoogle(service_account_creds=creds_data) as aiogoogle:
            self._service_sheets = await aiogoogle.discover("sheets", "v4")
            self._service_calendar = await aiogoogle.discover("calendar", "v3")
            self._service_drive = await aiogoogle.discover("drive", "v3")
        self._spreadsheet = self._service_sheets.spreadsheets
        self.aiogoogle = aiogoogle

    async def get_themes(self, chapter):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                             range=f"{chapter}!A2:B11")
            )
            values = res.get('values', [])
            return values

    async def get_theme_info(self, chapter, theme):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                             range=f"{chapter}!C{int(theme) + 1}:G{int(theme) + 1}")
            )
            values = res.get('values', [])
            return values[0]

    async def get_checkpoint(self, chapter):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                             range=f"{chapter}!I2:N2")
            )
            values = res.get('values', [])
            print("get_checkpoint- ", values[0])
            return values[0]

    async def get_knowledge(self, chapter):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.KNOWLEDGE_SPREADSHEET_ID,
                                             range=f"{chapter}!A2:B11")
            )
            values = res.get('values', [])
            print("get_knowledge- ", values)
            return values

    async def get_method_info(self, chapter, method_id):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.KNOWLEDGE_SPREADSHEET_ID,
                                             range=f"{chapter}!B{int(method_id) + 1}:C{int(method_id) + 1}")
            )
            values = res.get('values', [])
            print("get_method- ", values[0])
            return values[0]

    async def get_faq(self):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.FAQ_SPREADSHEET_ID,
                                             range=f"FAQ!A2:A")
            )

            values = res.get('values', [])
            print("get_FAQ- ", values)
            return values

    async def test_calendar(self):
        now = dt.datetime.utcnow().isoformat() + 'Z'
        try:
            async with self.aiogoogle as g:
                res = await g.as_service_account(
                    self._service_calendar.events.list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
                                        orderBy='startTime')
                )
                events = res.get('values', [])
                if not events:
                    print('No upcoming events found.')
                    return

                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)

