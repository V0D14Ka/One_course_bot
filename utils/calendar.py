import datetime


async def make_lessons_info(lessons):
    formatted_strings = []

    for item in lessons:
        datetime_string, auditorium = item
        datetime_obj = datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S%z')
        new_datetime_obj = datetime_obj + datetime.timedelta(hours=10)
        formatted_new = new_datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

        formatted_strings.append(f"{formatted_new} - {auditorium}")

    result = "\n".join(formatted_strings)
    result = "Расписание ближайших мероприятий:\n" + result
    return result


async def make_period_info(lessons, category):
    formatted_strings = []

    for item in lessons:
        datetime_string, auditorium, summary = item
        datetime_obj = datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S%z')
        new_datetime_obj = datetime_obj + datetime.timedelta(hours=10)
        formatted_new = new_datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

        formatted_strings.append(f"{formatted_new} - {auditorium} - {summary}")

    result = "\n".join(formatted_strings)
    result = f"Расписание мероприятий на {'неделю' if category == 'week' else 'месяц'}:\n" + result
    return result
