from typing import Union

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext

from DB.models import Users
from create_bot import teams_menu, google_api
from static.dictionaries import methods
from static.messages import make_method_info
from utils import check_access


async def teams(message: Union[types.CallbackQuery, types.Message]):
    # markup = await teams_menu.menu_keyboard()
    if isinstance(message, types.CallbackQuery):
        call = message
        try:

            user = await Users.get(id=message.from_user.id)
            if user.full_name is None or user.full_name == "":
                await call.message.edit_text("Вначале заполните данные о себе - /personal")
                return

            mesg, markup = await get_keyboard(message.from_user.id)
            await call.message.edit_text(mesg)
            await call.message.edit_reply_markup(markup)
        except MessageNotModified:
            pass

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return

        user = await Users.get(id=message.from_user.id)
        if user.full_name is None or user.full_name == "":
            await message.answer("Вначале заполните данные о себе - /personal")
            return

        mesg, markup = await get_keyboard(message.from_user.id)
        await message.answer(mesg, reply_markup=markup)


async def get_keyboard(user_id):
    user = await Users.get(id=user_id)
    print(user.team)
    if await user.team is None:
        markup = await teams_menu.menu_keyboard(True)
        return "Вы не состоите в команде", markup
    else:
        markup = await teams_menu.menu_keyboard(False)
        return "Вы в команде", markup


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню teams
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.
    method_id = callback_data.get('method_id')  # Номер метода

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await teams(call)

        case "1":
            if category == "1":
                if method_id == "1":
                    # Логика создания команды
                    pass
                else:
                    # Ищем команду
                    pass
            else:
                if method_id == "1":
                    # Смотрим участников
                    pass
                else:
                    # Покидаем группу
                    pass


def register_teams_handlers(_dp: Dispatcher):
    _dp.register_message_handler(teams, commands=['teams'])
    _dp.register_callback_query_handler(menu_navigate, teams_menu.menu_cd.filter(), state=None)
