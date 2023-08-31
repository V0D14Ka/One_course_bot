import os
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from DB.models import Users
from create_bot import topics_menu, google_api
from static import messages
from static.dictionaries import chapters, chapters_arr
from utils import check_access, check_cancel_update


class FSMSetDoc(StatesGroup):
    new_value = State()


async def topics(message: Union[types.CallbackQuery, types.Message]):
    markup = await topics_menu.menu_keyboard(chapters_arr)
    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Выберите раздел курса")
        await call.message.edit_reply_markup(markup)

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return
        await message.answer("Выберите раздел курса", reply_markup=markup)


async def doc_set(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        category = data["category"]
        call = data["call"]
        chapter = data["chapter"]

        if message.document.mime_type in ['application/pdf']:
            # Сохраняем файл
            user = await Users.get(id=message.from_user.id)
            file_path = os.path.join('saved_files', f"{user.full_name}.pdf")
            await message.document.download(destination=file_path)
            await call.message.edit_text("Файл успешно сохранен!")
        else:
            await call.message.edit_text("Неверный формат файла. Пожалуйста, отправьте PDF файл.")
            await message.delete()
            return

        await message.delete()
        await state.finish()


async def doc_set_text(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        call = data["call"]
        chapter = data["chapter"]

        # Обработка отмены
        if message.text.lower() == 'отмена':
            markup = await topics_menu.checkpoint_info(chapter)
            try:
                info = await google_api.get_checkpoint(chapters[f"{chapter}"])
                await call.message.edit_text(messages.example_cp % (info[0], info[1], info[2], info[3], info[4]))
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass
            await message.delete()
            await state.finish()
            return

        await call.message.edit_text("Отправьте документ в формате pdf или напишите 'отмена'")
        await message.delete()


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
    choose = callback_data.get('choose')

    await google_api.get_week_lessons()

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await topics(call)

        case "1":
            markup = await topics_menu.choose_category(chapter)
            try:
                await call.message.edit_text(f'Что вы хотите узнать в {chapters[f"{chapter}"]}?')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass

        case "2":
            if category == "1":
                themes = await google_api.get_themes(chapters[f"{chapter}"])
                markup = await topics_menu.choose_theme(chapter, themes)
                try:
                    await call.message.edit_text(f'Темы раздела {chapter}')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            elif category == "2":
                markup = await topics_menu.checkpoint_info(chapter)
                info = await google_api.get_checkpoint(chapters[f"{chapter}"])
                try:
                    await call.message.edit_text(messages.example_cp % (info[0], info[1], info[2], info[3], info[4]))
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            else:
                raise Exception("Не знаю такой категории")

        case "3":
            if category == "1":
                markup = await topics_menu.theme_info(chapter, theme)
                try:
                    await call.message.edit_text(f'Выберите пункт темы:')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            elif category == "2":
                try:
                    await call.message.edit_text(f'Загрузите файл в формате pdf или напишите "Отмена"')
                except MessageNotModified:
                    pass

                async with state.proxy() as data:
                    # Передаем необходимую информацию
                    data["category"] = category
                    data["call"] = call
                    data["chapter"] = chapter
                    await FSMSetDoc.new_value.set()

            else:
                raise Exception("Не знаю такой категории")

        case "4":
            info = await google_api.get_theme_info(chapters[f"{chapter}"], theme)
            markup = await topics_menu.back_keyboard(chapter, theme, category, 4)
            try:
                print(info, "-", choose)
                await call.message.edit_text(f'{info[int(choose)]}')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass


def register_topics_handlers(_dp: Dispatcher):
    _dp.register_message_handler(topics, commands=['topics'])
    _dp.register_message_handler(doc_set, state=FSMSetDoc.new_value, content_types=['document'])
    _dp.register_message_handler(doc_set_text, state=FSMSetDoc.new_value)
    _dp.register_callback_query_handler(menu_navigate, topics_menu.menu_cd.filter(), state=None)
