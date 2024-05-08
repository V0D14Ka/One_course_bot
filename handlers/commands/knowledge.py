from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from DB.models import Users
from create_bot import bot, knowledge_menu
from static import messages
from utils import check_access


async def knowledge(message: Union[types.CallbackQuery, types.Message]):
    markup = await knowledge_menu.menu_keyboard()

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
        Навигация по меню knowledge
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await knowledge(call)

        case "1":
            # Заглушка
            categories = {"1": "Список подразделов",
                          "2": "Список подразделов",
                          "3": "Список подразделов"}

            markup = await knowledge_menu.back_keyboard()
            try:
                await call.message.edit_text(categories[category])
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass


def register_knowledge_handlers(_dp: Dispatcher):
    _dp.register_message_handler(knowledge, commands=['knowledge'])
    _dp.register_callback_query_handler(menu_navigate, knowledge_menu.menu_cd.filter(), state=None)
