# Information
from DB.models import Users

welcome_mesg = '''Добро пожаловать в наш бот! Используйте /menu'''
help_mesg = '''Здесь будет инфа о командах бота'''
info_mesg = '''Здесь будет инфа о курсе'''

# Reply exceptions
cant_initiate_conversation = '''Для начала работы со мной напишите мне в ЛС!'''
bot_blocked = "Разблокируйте меня, чтобы продолжить диалог!"
unauthorized = 'Не удалось написать вам!'
went_wrong = 'Что-то пошло не так...'
incorrect_input = '''
Неверный ввод, попробуйте еще раз 
или напишите 'Отмена'!
Ошибка: %s.
Пример : %s.
'''

ask_for_update = '''
Для отмены напишите - "Отмена".
Текущее значение: %s. 
Введите новое значение: '''

ask_for_update_user_info = '''
Шаг %s/3.
Введите %s.
Пример : %s.
Для отмены напишите "Отмена". 
Обращаю ваше внимание: в случае отмены весь прогресс будет утерян.
'''

ask_for_update_user_group = '''
Шаг %s/3.
Введите %s.
Выберите группу из предложенных : %s.
Для отмены напишите "Отмена". 
Обращаю ваше внимание: в случае отмены весь прогресс будет утерян.
'''

example_cp = '''
1. Название тем: %s.
2. Список кейсов: %s.
3. Дата и время проведения контрольной точки: %s.
4. Аудитория %s.
5. Комментарий от преподавателя: %s'''

user_info = '''
Ваши личные данные:
ФИО - %s.
Курс - %s.
Группа - %s.
'''


async def make_user_info(item: Users, updated=False):
    """
    Сборка информации о студенте.
    :param item: Users.
    :param updated: Флаг - после изменения.
    :return: Строка с сообщением.
    """
    answer = user_info % (item.full_name, item.form, item.study_group)
    if updated:
        return "Изменение прошло успешно:\n" + answer
    else:
        return answer


async def make_method_info(info):
    input_string = info[1]
    books_list = input_string.split(';')
    formatted_string = '\n'.join([f'{index + 1}. {book},' for index, book in enumerate(books_list)])
    formatted_string = formatted_string[:-1]

    return f"{info[0]}:\n" + formatted_string


def format_faq_array_to_string(data):
    result = ""
    for index, item in enumerate(data, start=1):
        question, answer = item[0].split('-')
        result += f"{index}.'{question}'-{answer}\n"
    return result


def format_array_to_string(data):
    result = ""
    for item in data:
        result += f"{item},"
    return result[:-1]
