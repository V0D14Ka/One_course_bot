from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized
from aiogram.dispatcher import FSMContext

from create_bot import bot
from static import messages


async def personal(message: Union[types.CallbackQuery, types.Message]):

    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Выбрано о себе")
        # await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        await message.answer("Выбрано о себе")


def register_personal_handlers(_dp: Dispatcher):
    _dp.register_message_handler(personal, commands=['personal'])
