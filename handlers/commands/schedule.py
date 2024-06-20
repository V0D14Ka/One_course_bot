from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from keyboards import InlineMenu
from services.google_api import GoogleAPI
from utils import check_access
from utils.calendar import make_lessons_info, make_period_info


async def schedule(message: Union[types.CallbackQuery, types.Message]):

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        markup = await InlineMenu().schedule_menu.menu_keyboard()
        await message.answer("Выберите пункт", reply_markup=markup)

    if isinstance(message, types.CallbackQuery):
        call = message
        try:
            markup = await InlineMenu().schedule_menu.menu_keyboard()
            await call.message.edit_text("Выберите пункт")
            await call.message.edit_reply_markup(markup)
        except MessageNotModified:
            pass


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню расписания
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await schedule(call)

        case "1":
            # Заглушка
            categories = {"1": "Лекция",
                          "2": "Семинар",
                          "3": "КТ",
                          "4": "week",
                          "5": "month"}

            if category in "123":
                lessons = await GoogleAPI().get_lessons_dates(categories[category])
                answer = await make_lessons_info(lessons)
            else:
                lessons = await GoogleAPI().get_period_lessons(categories[category])
                answer = await make_period_info(lessons, categories[category])
            markup = await InlineMenu().schedule_menu.back_keyboard()

            try:
                await call.message.edit_text(answer)
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass


def register_schedule_handlers(_dp: Dispatcher):
    _dp.register_message_handler(schedule, commands=['schedule'])
    _dp.register_callback_query_handler(menu_navigate, InlineMenu().schedule_menu.menu_cd.filter(), state=None)
