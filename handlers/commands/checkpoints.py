from typing import Union

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from create_bot import bot, checkpoints_menu
from utils import check_access


async def checkpoints(message: Union[types.CallbackQuery, types.Message]):
    items = [["1", "КТ 1"], ["2", "КТ 2"], ["3", "КТ 3"]] # Тут мы будем доставать список КТ
    markup = await checkpoints_menu.menu_keyboard(items)

    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Выберите пункт")
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        await message.answer("Выберите пункт", reply_markup=markup)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню checkpoint
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.
    item_id = callback_data.get('item_id')

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await checkpoints(call)

        case "1":
            markup = await checkpoints_menu.choose_item(item_id)
            try:
                await call.message.edit_text(f'Выбран КТ {item_id}')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass

        case "2":
            markup = await checkpoints_menu.back_keyboard(item_id)
            try:
                await call.message.edit_text(f'Выбрано {category}')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass


def register_checkpoints_handlers(_dp: Dispatcher):
    _dp.register_message_handler(checkpoints, commands=['checkpoints'])
    _dp.register_callback_query_handler(menu_navigate, checkpoints_menu.menu_cd.filter(), state=None)
