import mimetypes
import os
import datetime
from datetime import timedelta
import asyncio
import json
import pprint

import aiohttp
from dotenv import load_dotenv
from aiogoogle import Aiogoogle
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

load_dotenv()


def load_creds_from_file(file_path):
    with open(file_path) as f:
        creds_data = json.load(f)
    return creds_data


class GoogleAPI:
    SERVICE_ACCOUNT_FILE = 'onecourseproject.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/calendar']
    TOPICS_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
    KNOWLEDGE_SPREADSHEET_ID = os.getenv("KNOWLEDGE_SPREADSHEET_ID")
    DAY_TASK_SPREADSHEET_ID = os.getenv("DAY_TASK_SPREADSHEET_ID")
    FAQ_SPREADSHEET_ID = os.getenv("FAQ_SPREADSHEET_ID")
    GROUP_SPREADSHEET_ID = os.getenv("GROUP_SPREADSHEET_ID")
    CALENDAR_ID = os.getenv("CALENDAR_ID")

    async def init(self):
        creds_data = load_creds_from_file(self.SERVICE_ACCOUNT_FILE)
        async with Aiogoogle(service_account_creds=creds_data) as aiogoogle:
            self._service_sheets = await aiogoogle.discover("sheets", "v4")
            self._service_calendar = await aiogoogle.discover("calendar", "v3")
            self._service_drive = await aiogoogle.discover("drive", "v3")
        self._spreadsheet = self._service_sheets.spreadsheets
        self.aiogoogle = aiogoogle

    async def get_themes(self, chapter):
        print(chapter)
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

    async def is_chapter_active(self, chapter):
        async with self.aiogoogle as g:
            error = await g.as_service_account(
                self._spreadsheet.values.get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                             range=f"{chapter}!H2")
            )

            value = error.get("values")

            if value is None or value[0][0] == '0':
                return False

            return True

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

    async def get_topics_chapters(self):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.get(spreadsheetId=self.TOPICS_SPREADSHEET_ID)
            )
            sheets = res.get('sheets', [])
            titles = [[item['properties']['index'], item['properties']['title']] for item in sheets]
            _titles = titles.copy()

            for sheet in titles:

                res = await g.as_service_account(
                    self._spreadsheet.values.get(spreadsheetId=self.TOPICS_SPREADSHEET_ID,
                                                 range=f"{sheet[1]}!H2")
                )

                value = res.get('values')

                # Проверяем флаг активности (Можно ли показывать раздел)
                if value is None or value[0][0] == '0':
                    _titles.remove(sheet)

            print("get_topics- ", titles, "\n", _titles)
            return _titles

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

    async def get_lessons_dates(self, summary):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        try:
            async with self.aiogoogle as g:
                res = await g.as_service_account(
                    self._service_calendar.events.list(calendarId=self.CALENDAR_ID, timeMin=now,
                                                       maxResults=5, singleEvents=True,
                                                       orderBy='startTime', q=summary)
                )
                events = res.get('items', [])
                if not events:
                    print('No upcoming events found.')
                    return []

                answer = []
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    try:
                        loc = event['location']
                    except:
                        loc = "Место неизвестно"
                    answer.append([start, loc])

                return answer

        except HttpError as error:
            print('An error occurred: %s' % error)

    async def get_period_lessons(self, period):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        current_date = datetime.datetime.utcnow()

        if period == "week":
            maxtime = (current_date + timedelta(weeks=1)).isoformat() + 'Z'
        elif period == "month":
            maxtime = (current_date + timedelta(days=30)).isoformat() + 'Z'
        try:
            async with self.aiogoogle as g:
                res = await g.as_service_account(
                    self._service_calendar.events.list(
                        calendarId=self.CALENDAR_ID,
                        timeMin=now,
                        timeMax=maxtime,
                        singleEvents=True,
                        orderBy='startTime')
                )
                events = res.get('items', [])

                if not events:
                    print('No upcoming events found.')
                    return []

                answer = []
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    try:
                        loc = event['location']
                    except:
                        loc = "Место неизвестно"
                    answer.append([start, loc, event['summary']])

                return answer

        except Exception as e:
            print('An error occurred: %s' % e)

    async def upload(self, file_url, username, folder_id, chapter=0):
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                    self._service_drive.files.list(q=f"'{folder_id}' in parents and mimeType='application/vnd.google"
                                                     f"-apps.folder'")
                )

            if 'files' in res:
                result = {item['name']: item['id'] for item in res['files']}
            else:
                return "error"

            try:
                upload_folder_id = result[f"{chapter}"]

                metadata = {
                    "name": username,
                    "parents": [upload_folder_id],
                }

                async with aiohttp.ClientSession():
                    await g.as_service_account(self._service_drive.files.create(
                        json=metadata,
                        upload_file=file_url,
                    ))

                return 200

            except:
                return "error"

    async def check_user(self, group, full_name):
        async with self.aiogoogle as g:
            try:
                res = await g.as_service_account(
                    self._spreadsheet.values.get(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                 range=f"{group}!B2:C")
                )
            except:
                return 500, 0

            values = res.get('values', [])

            count = 1
            for row in values:
                count += 1
                if full_name.lower() == (row[0]).lower():
                    try:
                        if row[1] is not None:
                            print("check_user - User is logged")
                            return 400, row[1]
                    except:
                        print(f"check_user - C{count}")
                        return 200, count

            print("check_user - student is not exist ")
            return 404, 0

    async def check_user_team(self, group, full_name):
        async with self.aiogoogle as g:
            try:
                res = await g.as_service_account(
                    self._spreadsheet.values.get(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                 range=f"{group}!B2:D")
                )
            except:
                return 500, 0

            values = res.get('values', [])

            count = 1
            for row in values:
                count += 1
                if full_name.lower() == (row[0]).lower():
                    try:
                        if row[2] is not None:
                            print("check_user_team - User is already in team")
                            return 400, row[2]
                    except:
                        print(f"check_user - D{count}")
                        return 200, count

            print("check_user_team - student is not exist ")
            return 404, 0

    async def get_team_col(self, group, full_name):
        async with self.aiogoogle as g:
            try:
                res = await g.as_service_account(
                    self._spreadsheet.values.get(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                 range=f"{group}!B2:D")
                )
            except:
                return 500, 0
            values = res.get('values', [])
            count = 1
            for row in values:
                count += 1
                if full_name.lower() == (row[0]).lower():
                    print(f"get_team_col - student {full_name} - D{count}")
                    return 200, count

            print("get_team_col - student is not exist ")
            return 404, 0

    async def delete_team(self, team):
        async with self.aiogoogle as g:
            # try:
            # Получить список всех листов в таблице
            spreadsheet_info = await g.as_service_account(
                self._spreadsheet.get(spreadsheetId=self.GROUP_SPREADSHEET_ID)
            )
            sheets = spreadsheet_info.get('sheets', [])
            titles = [item['properties']['title'] for item in sheets]

            # Пройти по всем листам и выполнить запрос для каждого
            for sheet in titles:
                result = []
                value_range_body = {
                    'values': [[""]]
                }

                res = await g.as_service_account(
                    self._spreadsheet.values.get(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                 range=f"{sheet}!B2:D")
                )

                values = res.get('values', [])
                count = 1

                for row in values:
                    count += 1
                    try:
                        if team == row[2]:
                            result.append(count)
                    except:
                        pass

                for i in result:
                    await g.as_service_account(
                        self._spreadsheet.values.update(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                        range=f"{sheet}!D{i}", json=value_range_body,
                                                        valueInputOption='USER_ENTERED')
                    )
                    print(f"delete-team {team} : col - {i}, group - {sheet}")

            return result

        # except Exception as e:
        #     print(f"An error occurred: {e}")
        #     return 500, 1

    async def set_id(self, tg_id, col, group):
        value_range_body = {
            'values': [[tg_id]]
        }
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.update(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                range=f"{group}!C{col}", json=value_range_body,
                                                valueInputOption='USER_ENTERED')
            )
            print(f"set-id : col - {col}, tg_id - {tg_id}, group - {group}")

            return

    async def set_team(self, admin, col, group):
        value_range_body = {
            'values': [[admin]]
        }
        async with self.aiogoogle as g:
            res = await g.as_service_account(
                self._spreadsheet.values.update(spreadsheetId=self.GROUP_SPREADSHEET_ID,
                                                range=f"{group}!D{col}", json=value_range_body,
                                                valueInputOption='USER_ENTERED')
            )
            print(f"set-team : col - {col}, team_id - {admin}, group - {group}")

            return
