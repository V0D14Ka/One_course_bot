from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from DB.models import Users, Teams
from create_bot import teams_menu, google_api, validation
from static.dictionaries import methods
from static.messages import make_method_info
from utils import check_access, check_cancel_update, check_validate


class FSMfindTeam(StatesGroup):
    team_pass = State()


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

    if await user.team is None:
        markup = await teams_menu.menu_keyboard(True)
        return "Вы не состоите в команде", markup
    else:
        team = await user.team

        if await Teams.exists(admin=user_id):
            markup = await teams_menu.menu_keyboard(False, team.id)
            return f"Вы в команде, код для вступления в команду - {user_id}", markup

        markup = await teams_menu.menu_keyboard(False, team.id)
        return "Вы в команде", markup


async def find_team(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        category = data["category"]
        call = data["call"]
        new_value = message.text
        # И кладем новую
        data["form"] = new_value

        # Обработка отмены
        if message.text.lower() == 'отмена':
            await check_cancel_update(call, message, state, category, teams)
            return

        # Обработка ошибки валидации
        code = await validation.val_digit(new_value)

        if code != 200:
            await check_validate(call, message, code, "'111111111'")
            return

        try:
            team = await Teams.get(admin=int(new_value))
        except:
            await call.message.edit_text("Такая группа не обнаружена, попробуйте снова или напишите 'отмена'")
            await message.delete()
            return

        if team.count == 3:
            await call.message.edit_text("Все места в группе уже заняты, попробуйте другую или напишите 'отмена'")
            await message.delete()
            return

        user = await Users.get(id=message.from_user.id)
        user.team = team
        team.count += 1
        await team.save()
        await user.save()

        await message.delete()
        await state.finish()
        await teams(call)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню teams
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.
    method_id = callback_data.get('method_id')  # Номер метода
    team_id = callback_data.get('team_id')  # Team id

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await teams(call)

        case "1":
            if category == "1":
                if method_id == "1":
                    # Логика создания команды
                    try:
                        team = await Teams.create(admin=call.from_user.id)
                        user = await Users.get(id=call.from_user.id)
                        user.team = team
                        await user.save()
                        await teams(call)
                    except Exception as e:
                        raise e
                    return
                else:
                    await call.message.edit_text("Напишите код для вступления в команду.")
                    async with state.proxy() as data:
                        # Передаем необходимую информацию
                        data["category"] = category
                        data["call"] = call
                        await FSMfindTeam.team_pass.set()
            else:
                if method_id == "1":
                    # Смотрим участников
                    users = await Users.filter(team=team_id).values("id", "full_name", "study_group")
                    markup = await teams_menu.back_keyboard(category=category, level=1)
                    if len(users) != 0:
                        ans = ""
                        i = 1
                        for user in users:
                            ans += (f'{i}.' + hlink(str(user["full_name"]), f"tg://openmessage?user_id={user['id']}")
                                    + ", " + str(user["study_group"]) + '.\n')
                            i += 1
                        await call.message.edit_text(ans, parse_mode=types.ParseMode.HTML)
                    else:
                        await call.message.edit_text("Список пуст :(")

                    await call.message.edit_reply_markup(markup)

                else:
                    # Покидаем группу
                    pass


def register_teams_handlers(_dp: Dispatcher):
    _dp.register_message_handler(teams, commands=['teams'])
    _dp.register_callback_query_handler(menu_navigate, teams_menu.menu_cd.filter(), state=None)
    _dp.register_message_handler(find_team, state=FSMfindTeam.team_pass)
