from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from create_bot import bot, topics_menu
from static import messages


async def topics(message: Union[types.CallbackQuery, types.Message]):
    arr = [["1", "Раздел 1"], ["2", "Раздел 2"], ["3", "Раздел 3"]]
    markup = await topics_menu.menu_keyboard(arr)
    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Выберите раздел курса")
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        await message.answer("Выберите раздел курса", reply_markup=markup)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню checkpoint
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.
    item_id = callback_data.get('item_id')
    chapter = callback_data.get('chapter')
    theme = callback_data.get('theme')

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await topics(call)

        case "1":
            markup = await topics_menu.choose_category(chapter)
            try:
                await call.message.edit_text(f'Что вы хотите узнать в разделе {chapter}?')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass

        case "2":
            if category == "1":
                themes = [["1", "Тема 1"], ["2", "Тема 2"], ["3", "Тема 3"]]
                markup = await topics_menu.choose_theme(chapter, themes)
                try:
                    await call.message.edit_text(f'Темы раздела {chapter}')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            elif category == "2":
                markup = await topics_menu.checkpoint_info(chapter)
                try:
                    await call.message.edit_text(messages.example_cp)
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            else:
                raise Exception("Не знаю такой категории")

        case "3":
            if category == "1":
                markup = await topics_menu.theme_info(chapter, theme)
                try:
                    await call.message.edit_text(f'Выберите пункт темы {theme}')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            elif category == "2":
                markup = await topics_menu.back_keyboard(chapter, theme, category, 3)
                try:
                    await call.message.edit_text(f'Здесь будут инфа + ссылки')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            else:
                raise Exception("Не знаю такой категории")

        case "4":
            markup = await topics_menu.back_keyboard(chapter, theme, category, 4)
            try:
                await call.message.edit_text(f'Здесь будут инфа + ссылки')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass


def register_topics_handlers(_dp: Dispatcher):
    _dp.register_message_handler(topics, commands=['topics'])
    _dp.register_callback_query_handler(menu_navigate, topics_menu.menu_cd.filter(), state=None)
