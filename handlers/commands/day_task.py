from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import day_task_menu
from services.google_api import GoogleAPI
from utils import check_access


async def day_task(message: Union[types.CallbackQuery, types.Message]):
    markup = await day_task_menu.menu_keyboard()
    task = await GoogleAPI().get_day_task()
    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(task)
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        await message.answer(task, reply_markup=markup)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню knowledge
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await day_task(call)


def register_day_task_handlers(_dp: Dispatcher):
    _dp.register_message_handler(day_task, commands=['day_task'])
    _dp.register_callback_query_handler(menu_navigate, day_task_menu.menu_cd.filter(), state=None)
