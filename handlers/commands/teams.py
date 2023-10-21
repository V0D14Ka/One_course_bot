from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.markdown import hlink

from DB.models import Users, Teams
from keyboards import InlineMenu
from services.google_api import GoogleAPI
from utils import check_access, check_cancel_update, check_validate, Validation


class FSMfindTeam(StatesGroup):
    team_pass = State()


class FSMDeleteTeam(StatesGroup):
    sure = State()


class FSMLeaveTeam(StatesGroup):
    sure = State()


async def teams(message: Union[types.CallbackQuery, types.Message]):

    if isinstance(message, types.Message):
        if await check_access(message) is False:
            return

        user = await Users.get(id=message.from_user.id)
        if user.full_name is None or user.full_name == "":
            await message.answer("Вначале заполните данные о себе - /personal")
            return

        mesg, markup = await get_keyboard(message.from_user.id)
        await message.answer(mesg, reply_markup=markup)

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


async def get_keyboard(user_id):
    user = await Users.get(id=user_id)

    if await user.team is None:
        markup = await InlineMenu().teams_menu.menu_keyboard(True)
        return "Вы не состоите в команде", markup

    else:
        team = await user.team

        if await Teams.exists(admin=user_id):
            if await Teams.get(admin=user_id) == team:
                markup = await InlineMenu().teams_menu.menu_keyboard(False, team.id)
                return f"Вы в команде, код для вступления в команду - {user_id}", markup

        markup = await InlineMenu().teams_menu.menu_keyboard(False, team.id)
        return "Вы в команде", markup


async def check_team(call, group, full_name):
    status, col = await GoogleAPI().check_user_team(group, full_name)
    match status:
        case 400:
            await call.message.edit_text(
                "Вы уже состоите в группе, покиньте предыдущую и попробуйте снова.")
            return 1, 1

        case 200:
            return 200, col
        case 404:
            await call.message.edit_text(
                "Произошла ошибка, вы не были найдены в списке вашей учебной группы")
            return 1, 1

        case 500:
            await call.message.edit_text(
                "Произошла непридвиденная ошибка, попробуйте позже")
            return 1, 1


async def find_team(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        category = data["category"]
        call = data["call"]
        new_value = message.text

        # Обработка отмены
        if message.text.lower() == 'отмена':
            await check_cancel_update(call, message, state, category, teams)
            return

        # Обработка ошибки валидации
        code = await Validation().val_digit(new_value)

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

        status, col = await check_team(call=call, group=user.study_group, full_name=user.full_name)

        if status != 200:
            await state.finish()
            await message.delete()
            return

        await GoogleAPI().set_team(team.admin, col, user.study_group)
        user.team = team
        team.count += 1
        await team.save()
        await user.save()

        await message.delete()
        await state.finish()
        await teams(call)


async def team_create(call, user_id):
    try:
        user = await Users.get(id=user_id)
        status, col = await check_team(call=call, group=user.study_group, full_name=user.full_name)

        if status != 200:
            return

        team = await Teams.create(admin=user_id)
        await GoogleAPI().set_team(user_id, col, user.study_group)

        user.team = team
        await user.save()
        await teams(call)

    except Exception as e:
        raise e


async def team_delete(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        call = data["call"]
        team_id = data["team_id"]

        if message.text.lower() == "да":
            team = await Teams.get(id=team_id)
            await GoogleAPI().delete_team(team.admin)
            await team.delete()

        try:
            await message.delete()
        except:
            pass

        await state.finish()
        await teams(call)


async def team_leave(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        call = data["call"]
        team_id = data["team_id"]

        if message.text.lower() == "да":

            team = await Teams.get(id=team_id)
            user = await Users.get(id=call.from_user.id)

            status, col = await GoogleAPI().get_team_col(user.study_group, user.full_name)

            if status == 200:
                await GoogleAPI().set_team("", col, user.study_group)
                user.team = None
                team.count -= 1
                await user.save()
                await team.save()

            else:
                await call.message.edit_text("Произошла непредвиденная ошибка, попробуйте позже")
                await message.delete()
                await state.finish()
                return

        try:
            await message.delete()
        except:
            pass

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
                    await team_create(call, call.from_user.id)
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
                    markup = await InlineMenu().teams_menu.back_keyboard(category=category, level=1)
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

                    try:
                        team = await Teams.get(id=team_id)
                    except:
                        await call.message.edit_text("Произошла ошибка, возможно вы пытались использовать старое меню.")
                        return

                    if call.from_user.id == int(team.admin):
                        await call.message.edit_text(
                            "Вы являетесь капитаном данной команды, если вы ее покините, команда будет удалена, "
                            "вы уверены? Напишите 'Да' для удаления, любой другой текст будет воспринят как отмена.")
                        async with state.proxy() as data:
                            # Передаем необходимую информацию
                            data['team_id'] = team_id
                            data["call"] = call
                            await FSMDeleteTeam.sure.set()
                            return

                    await call.message.edit_text(
                        "Вы действительно хотите покинуть команду? Напишите 'Да' для подтверждения"
                        ", любой другой текст будет воспринят как отмена.")
                    async with state.proxy() as data:
                        # Передаем необходимую информацию
                        data['team_id'] = team_id
                        data["call"] = call
                        await FSMLeaveTeam.sure.set()
                        return


def register_teams_handlers(_dp: Dispatcher):
    _dp.register_message_handler(teams, commands=['teams'])
    _dp.register_callback_query_handler(menu_navigate, InlineMenu().teams_menu.menu_cd.filter(), state=None)
    _dp.register_message_handler(find_team, state=FSMfindTeam.team_pass)
    _dp.register_message_handler(team_delete, state=FSMDeleteTeam.sure)
    _dp.register_message_handler(team_leave, state=FSMLeaveTeam.sure)
