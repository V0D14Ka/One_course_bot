from typing import Union

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from create_bot import topics_menu, google_api
from utils import check_access


async def checkpoints(message: Union[types.CallbackQuery, types.Message]):
    # items = [["1", "КТ 1"], ["2", "КТ 2"], ["3", "КТ 3"]] # Тут мы будем доставать список КТ
    items = await google_api.get_topics_chapters()
    markup = await topics_menu.menu_cp_keyboard(items)

    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Выберите пункт")
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        await message.answer("Выберите пункт", reply_markup=markup)


def register_checkpoints_handlers(_dp: Dispatcher):
    _dp.register_message_handler(checkpoints, commands=['checkpoints'])
