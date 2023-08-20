from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized
from aiogram.dispatcher import FSMContext

from create_bot import faq_menu


async def faq(message: Union[types.CallbackQuery, types.Message]):
    markup = await faq_menu.menu_keyboard()
    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Тут будет список вопрос-ответ")
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        await message.answer("Тут будет список вопрос-ответ", reply_markup=markup)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню knowledge
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await faq(call)


def register_faq_handlers(_dp: Dispatcher):
    _dp.register_message_handler(faq, commands=['FAQ', 'faq'])
    _dp.register_callback_query_handler(menu_navigate, faq_menu.menu_cd.filter(), state=None)
