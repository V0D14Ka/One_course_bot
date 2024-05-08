from aiogram import types

from DB.models import Users


async def check_access(message: types.Message):
    if not await Users.exists(id=message.from_user.id):
        await message.answer("Для начала работы напишите /start")
        try:
            await message.delete()
        except:
            pass
        return False
    return True
