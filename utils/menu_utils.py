from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, MessageCantBeDeleted

from DB.models import Users
from static import messages


async def check_access(message: types.Message):
    if not await Users.exists(id=message.from_user.id):
        await message.answer("Для начала работы напишите /start")
        try:
            await message.delete()
        except:
            pass
        return False
    return True


async def check_blank_user_info(user_id):
    user = await Users.get(id=user_id)
    if user.full_name is None or user.full_name == '':
        mesg = "Вы еще не заполнили информацию о себе"
        flag = False
    else:
        mesg = await messages.make_user_info(user, updated=False)
        flag = True

    return mesg, flag


async def check_validate(call: types.CallbackQuery, message: types.Message, code, example):
    """
       Универсальная обработка ошибки валидации
    """
    try:
        await call.message.edit_text(messages.incorrect_input % (code, example))
    except MessageNotModified:
        pass

    try:
        await message.delete()
    except MessageCantBeDeleted:
        pass

    return True

async def check_cancel_update(call: types.CallbackQuery, message: types.Message, state: FSMContext, category, personal):
    """
        Обработка отмены, выход из состояния и возврат в меню
    """
    try:
        await personal(call)
        await message.delete()
        await state.finish()
    except MessageCantBeDeleted:
        pass
    return True
