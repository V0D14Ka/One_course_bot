import os
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

from keyboards import InlineMenu
from services.google_api import GoogleAPI
from static.messages import make_method_info, format_array_to_string
from utils import check_access

load_dotenv()


async def faq(message: Union[types.CallbackQuery, types.Message]):
    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        info = await GoogleAPI().get_faq()
        answer = await format_array_to_string(info)
        markup = InlineKeyboardMarkup()
        teacher_id = os.getenv("teacher_id")
        markup.row(
            InlineKeyboardButton(text="Написать преподавателю", url=f"tg://openmessage?user_id={teacher_id}")
        )
        await message.answer(answer, reply_markup=markup)

    if isinstance(message, types.CallbackQuery):
        call = message
        info = await GoogleAPI().get_faq()
        answer = await format_array_to_string(info)
        markup = InlineKeyboardMarkup()
        teacher_id = os.getenv("teacher_id")
        markup.row(
            InlineKeyboardButton(text="Написать преподавателю", url=f"tg://openmessage?user_id={teacher_id}")
        )
        await call.message.edit_text(answer)
        await call.message.edit_reply_markup(markup)


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
    _dp.register_callback_query_handler(menu_navigate, InlineMenu().faq_menu.menu_cd.filter(), state=None)
