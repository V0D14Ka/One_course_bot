from typing import Union

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from keyboards import InlineMenu
from services.google_api import GoogleAPI
from utils import check_access


async def checkpoints(message: Union[types.CallbackQuery, types.Message]):

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        items = await GoogleAPI().get_topics()
        markup = await InlineMenu().topics_menu.menu_cp_keyboard(items)
        await message.answer("Выберите пункт", reply_markup=markup)

    if isinstance(message, types.CallbackQuery):
        call = message
        items = await GoogleAPI().get_topics()
        markup = await InlineMenu().topics_menu.menu_cp_keyboard(items)
        await call.message.edit_text("Выберите раздел курса, КТ которого Вас интересует")
        await call.message.edit_reply_markup(markup)


def register_checkpoints_handlers(_dp: Dispatcher):
    _dp.register_message_handler(checkpoints, commands=['checkpoints'])
