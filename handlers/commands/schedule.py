from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from DB.models import Users
from create_bot import bot, schedule_menu
from static import messages
from utils import check_access


async def schedule(message: Union[types.CallbackQuery, types.Message]):
    markup = await schedule_menu.menu_keyboard()

    if isinstance(message, types.CallbackQuery):
        call = message
        try:
            await call.message.edit_text("Выберите пункт")
            await call.message.edit_reply_markup(markup)
        except MessageNotModified:
            pass

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        await message.answer("Выберите пункт", reply_markup=markup)


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
            categories = {"1": "Расписание лекций",
                          "2": "Расписание семенаров",
                          "3": "Расписание КТ",
                          "4": "На ближайшую неделю",
                          "5": "На ближайший месяц"}

            markup = await schedule_menu.back_keyboard()
            try:
                await call.message.edit_text(categories[category])
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass


def register_schedule_handlers(_dp: Dispatcher):
    _dp.register_message_handler(schedule, commands=['schedule'])
    _dp.register_callback_query_handler(menu_navigate, schedule_menu.menu_cd.filter(), state=None)
