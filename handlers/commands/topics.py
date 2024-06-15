import io
import os
from typing import Union

import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseUpload

from DB.models import Users, Teams
from create_bot import topics_menu, bot
from services.google_api import GoogleAPI
from static import messages
from utils import check_access, check_cancel_update

load_dotenv()


class FSMSetDoc(StatesGroup):
    new_value = State()


async def topics(message: Union[types.CallbackQuery, types.Message]):
    chapters_arr = await GoogleAPI().get_topics()
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
            if message.document.file_size < 83886080:
                # Сохраняем файл
                await call.message.edit_text("Пожалуйста подождите загрузки файла🕒")
                await state.finish()
                user = await Users.get(id=message.from_user.id)

                # Дополнительная проверка на случай использования старого меню
                if not await Teams.exists(admin=user.id):
                    await call.message.edit_text("Чтобы отправить файл на проверку, необходимо быть лидером команды")
                    await message.delete()
                    return

                username = user.study_group + '. ' + user.full_name + '. ' + str(user.id)
                file_info = await bot.get_file(message.document.file_id)

                BOT_TOKEN = os.getenv("TOKEN")
                file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
                response = requests.get(file_url, stream=True)

                folder_id = os.getenv("CHECKPOINTS_FOLDER")
                response = await GoogleAPI().upload(io.BytesIO(response.content).getvalue(), username, folder_id,
                                                   chapter)
                if response != "error":
                    await call.message.edit_text("Файл успешно сохранен!✅")
                else:
                    await call.message.edit_text("В данный момент прием работ не принимается")

        else:
            await call.message.edit_text("Неверный формат файла❌. Пожалуйста, отправьте файл в формате PDF.")
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
                info = await GoogleAPI().get_checkpoint(chapter)
                await call.message.edit_text(messages.example_cp % (info[0], info[1], info[2], info[3], info[4]))
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass
            await message.delete()
            await state.finish()
            return

        try:
            await call.message.edit_text("Отправьте документ в формате pdf или напишите 'отмена'")
        except MessageNotModified:
            pass

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
    upload = callback_data.get('upload')

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await topics(call)

        case "1":
            markup = await topics_menu.choose_category(chapter)
            try:
                await call.message.edit_text(f'Что вы хотите узнать в {chapter}?')
                await call.message.edit_reply_markup(markup)
            except MessageNotModified:
                pass

        case "2":
            is_active = await GoogleAPI().is_chapter_active(chapter)
            print(f"Level 2, Chapter: {chapter}, is active :{is_active}")
            if not is_active:
                try:
                    await call.message.edit_text(f'В данный момент нельзя взаимодействовать с {chapter}')
                    markup = await topics_menu.back_keyboard(chapter, theme, category, level=1)
                    await call.message.edit_reply_markup(markup)
                    return
                except MessageNotModified:
                    pass

            if category == "1":
                themes = await GoogleAPI().get_themes(chapter)
                markup = await topics_menu.choose_theme(chapter, themes)
                try:
                    await call.message.edit_text(f'Темы раздела {chapter}')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            elif category == "2":
                if await Teams.exists(admin=call.from_user.id):
                    is_lead = True
                else:
                    is_lead = False

                info = await GoogleAPI().get_checkpoint(chapter)
                markup = await topics_menu.checkpoint_info(chapter, is_lead)
                try:
                    info = info[0]
                    await call.message.edit_text(messages.example_cp % (info[0], info[1], info[2], info[3], info[4]))
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass
                except:
                    await call.message.edit_text(f"В данный момент нет информации о КТ {chapter}")
                    await call.message.edit_reply_markup(markup)


            else:
                raise Exception("Не знаю такой категории")

        case "3":

            is_active = await GoogleAPI().is_chapter_active(chapter)
            print(f"Level 3, Chapter: {chapter}, is active :{is_active}")
            if not is_active:
                try:
                    await call.message.edit_text(f'В данный момент нельзя взаимодействовать с {chapter}')
                    markup = await topics_menu.back_keyboard(chapter, theme, category, level=1)
                    await call.message.edit_reply_markup(markup)
                    return
                except MessageNotModified:
                    pass

            if category == "1":
                markup = await topics_menu.theme_info(chapter, theme)
                try:
                    await call.message.edit_text(f'Выберите пункт темы:')
                    await call.message.edit_reply_markup(markup)
                except MessageNotModified:
                    pass

            elif category == "2":
                if upload == "1":
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
                    info = await GoogleAPI().get_checkpoint(chapter)
                    markup = await topics_menu.back_keyboard(chapter, theme, category, 3)
                    try:
                        await call.message.edit_text(f'{info[-1]}')
                        await call.message.edit_reply_markup(markup)
                    except MessageNotModified:
                        pass

            else:
                raise Exception("Не знаю такой категории")

        case "4":

            is_active = await GoogleAPI().is_chapter_active(chapter)
            print(f"Level 4, Chapter: {chapter}, is active :{is_active}")
            if not is_active:
                try:
                    await call.message.edit_text(f'В данный момент нельзя взаимодействовать с {chapter}')
                    markup = await topics_menu.back_keyboard(chapter, theme, category, level=1)
                    await call.message.edit_reply_markup(markup)
                    return
                except MessageNotModified:
                    pass

            info = await GoogleAPI().get_theme_info(chapter, theme)
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
