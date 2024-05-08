from typing import Union

from aiogram import types, Dispatcher
from static import messages


async def info(message: Union[types.CallbackQuery, types.Message]):

    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(messages.info_mesg)
        # await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        await message.answer(messages.info_mesg)


def register_info_handlers(_dp: Dispatcher):
    _dp.register_message_handler(info, commands=['info'])
