from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized, \
    MessageNotModified
from aiogram.dispatcher import FSMContext
from tortoise.exceptions import NoValuesFetched

from DB.models import Users
from create_bot import bot, personal_menu, validation, google_api
from static import messages
from utils import check_access
from utils import check_blank_user_info, check_validate, check_cancel_update


class FSMUpdateUserInfo(StatesGroup):
    """
       Состояния первоначального регистрирования информации о студенте
    """
    study_group = State()
    form = State()
    full_name = State()


class FSMUpdateUserValue(StatesGroup):
    """
       Состояние обновления поля студента
    """
    new_value = State()


# Далее FSM
async def group_set(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        category = data["category"]
        call = data["call"]
        new_value = message.text
        # И кладем новую
        data["group"] = new_value

        # Обработка отмены
        if message.text.lower() == 'отмена':
            await check_cancel_update(call, message, state, category, personal)
            return

        # Обработка ошибки валидации
        code = await validation.val_mix(new_value)

        if code != 200:
            await check_validate(call, message, code, "'Б9121'")
            return

        await message.delete()
        await call.message.edit_text(messages.ask_for_update_user_info % ("2", "Номер курса", "'2'"))
        await FSMUpdateUserInfo.next()


async def form_set(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию
        category = data["category"]
        call = data["call"]
        new_value = message.text
        # И кладем новую
        data["form"] = new_value

        # Обработка отмены
        if message.text.lower() == 'отмена':
            await check_cancel_update(call, message, state, category, personal)
            return

        # Обработка ошибки валидации
        code = await validation.val_digit(new_value)

        if code != 200:
            await check_validate(call, message, code, "'2'")
            return

        await message.delete()
        await call.message.edit_text(messages.ask_for_update_user_info % ("3", "ФИО", "'Иванов Иван Иванович'"))
        await FSMUpdateUserInfo.next()


async def fullname_set(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        # Забираем необходимую информацию на случай отмены
        category = data["category"]
        call = data["call"]
        new_value = message.text

        # Обработка отмены
        if message.text.lower() == 'отмена':
            await check_cancel_update(call, message, state, category, personal)
            return

        # Обработка ошибки валидации
        code = await validation.val_fio(new_value)

        if code != 200:
            await check_validate(call, message, code, "'Иванов Иван Иванович'")
            return

        # Забираем инфу о пользователе
        group = data["group"]
        full_name = new_value
        form = data["form"]

        status, tg = await google_api.check_user(group, full_name)
        match status:
            case 400:
                if str(message.from_user.id) != tg:
                    await personal(call, error="Такой студент уже зарегистрирован под другим telegram_id")
                    try:
                        await message.delete()
                    except:
                        pass
                    await state.finish()
                    return

            case 200:
                await call.message.edit_text("Аутентификация успешна")
            case 404:
                await personal(call, error="Студент с данным именем, в данной группе не найден")
                try:
                    await message.delete()
                except:
                    pass
                await state.finish()
                return
            case 500:
                await personal(call, error="Такая группа не существует, проверьте правильность введенных данных и попробуйте сначала")
                try:
                    await message.delete()
                except:
                    pass
                await state.finish()
                return

        # Сохраняем пользователя
        try:
            user = await Users.get(id=message.from_user.id)
            user.full_name = full_name
            user.study_group = group
            user.form = form
            await user.save()
        except NoValuesFetched as e:
            raise e

        try:
            await message.delete()
        except:
            pass

        await personal(call)
        await state.finish()


# Обновление одного поля
# async def on_update_user(message: types.Message, state: FSMContext, **kwargs):
#     """
#        Обработка введенного значения для изменения информации о пользователе
#     """
#     async with state.proxy() as data:
#
#         # Забираем необходимую информацию
#         change = data["change"]
#         category = data["category"]
#         call = data["call"]
#         new_value = message.text
#
#         # Обработка отмены
#         if message.text.lower() == 'отмена':
#             await check_cancel_update(call, message, state, category, personal)
#             return
#
#         # Валидация
#         if change == "1":
#             code = await validation.val_fio(new_value)
#             example = "Иванов Иван Иванович"
#         elif change == "2":
#             code = await validation.val_digit(new_value)
#             example = "2"
#         elif change == "3":
#             code = await validation.val_mix(new_value)
#             example = "Б0101-01.01.01"
#
#         # Проверка полученного кода
#         if code != 200:
#             await check_validate(call, message, code, example)
#             return
#
#         # Изменение курса, если сюда пришло, значит проблем нет
#         user = await Users.get(id=message.from_user.id)
#         user[int(change)] = new_value
#
#         try:
#             await user.save()
#             await personal(call, changed=True)
#         except:
#             await bot.send_message(message.from_user.id, messages.went_wrong)
#         await state.finish()
#
#         try:
#             await message.delete()
#         except MessageCantBeDeleted:
#             pass


async def personal(message: Union[types.CallbackQuery, types.Message], changed=False, error=False):
    if await check_access(message) is False:
        return
    mesg, flag = await check_blank_user_info(message.from_user.id)

    if error:
        mesg = error

    if changed:
        mesg = "Обновление прошло успешно\n" + mesg

    markup = await personal_menu.menu_keyboard(flag)

    if isinstance(message, types.CallbackQuery):
        try:
            await message.message.edit_text(mesg)
            if not flag:
                await message.message.edit_reply_markup(markup)
        except MessageNotModified:
            pass

    if isinstance(message, types.Message):
        await message.answer(mesg, reply_markup=markup)


async def menu_navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """
        Навигация по меню расписания
    """
    # Достаем информацию из колбека
    current_level = callback_data.get('level')  # Текущий уровень меню.
    category = callback_data.get('category')  # Текущая категория.
    change = callback_data.get('change')

    # Смотрим какой уровень был вызван
    match current_level:

        case "0":
            await personal(call)

        case "1":
            if category == "2":
                await call.message.edit_text(messages.ask_for_update_user_info % ("1", "Номер группы", "'Б9121'"))
                async with state.proxy() as data:
                    # Передаем необходимую информацию
                    data["category"] = category
                    data["call"] = call
                    await FSMUpdateUserInfo.study_group.set()
            else:
                try:
                    markup = await personal_menu.to_change_keyboard()
                    await call.message.edit_text("Что вы хотите изменить?")
                    await call.message.edit_reply_markup(markup)
                except:
                    pass

        case "2":
            item = await Users.get(id=call.from_user.id)
            await call.message.edit_text(messages.ask_for_update % item[int(change)])
            async with state.proxy() as data:
                # Передаем необходимую информацию
                data["category"] = category
                data["call"] = call
                data["change"] = change
                await FSMUpdateUserValue.new_value.set()


def register_personal_handlers(_dp: Dispatcher):
    _dp.register_message_handler(personal, commands=['personal'])
    _dp.register_message_handler(fullname_set, state=FSMUpdateUserInfo.full_name)
    _dp.register_message_handler(form_set, state=FSMUpdateUserInfo.form)
    _dp.register_message_handler(group_set, state=FSMUpdateUserInfo.study_group)
    # _dp.register_message_handler(on_update_user, state=FSMUpdateUserValue.new_value)
    _dp.register_callback_query_handler(menu_navigate, personal_menu.menu_cd.filter(), state=None)
