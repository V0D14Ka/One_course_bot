import os
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

from create_bot import faq_menu, google_api
from static.messages import make_method_info, format_array_to_string
from utils import check_access

load_dotenv()


async def faq(message: Union[types.CallbackQuery, types.Message]):
    info = await google_api.get_faq()
    answer = await format_array_to_string(info)
    markup = InlineKeyboardMarkup()
    teacher_id = os.getenv("teacher_id")
    markup.row(
        InlineKeyboardButton(text="Написать преподавателю", url=f"tg://openmessage?user_id={teacher_id}")
    )
    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(answer)
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        await message.answer(answer, reply_markup=markup)


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
