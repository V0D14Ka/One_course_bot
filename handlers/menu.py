from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from create_bot import bot, inline_menu
from handlers.commands import *
from static import messages


async def list_categories(message: Union[types.CallbackQuery, types.Message], **kwargs):
    """
       Корректная выдача меню
    """
    markup = await inline_menu.menu_keyboard()

    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        await message.answer("Выберите пункт меню:", reply_markup=markup)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню админа
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await call.message.edit_text("Выберите пункт")
            await list_categories(call)

        case "1":
            categories = {"1": topics,
                          "2": checkpoints,
                          "3": info,
                          "4": schedule,
                          "5": day_task,
                          "6": knowledge,
                          "7": personal}

            await categories[category](call)


def register_handlers_menu(_dp: Dispatcher):
    _dp.register_message_handler(list_categories, commands=['menu'])
    _dp.register_callback_query_handler(menu_navigate, inline_menu.menu_cd.filter(), state=None)