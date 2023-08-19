from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageCantBeDeleted, CantInitiateConversation, BotBlocked, Unauthorized
from aiogram.dispatcher import FSMContext

from create_bot import bot
from static import messages


async def commands_start(message: types.Message):
    """
        Обработка команд start/help
    """
    try:
        msg = messages.welcome_mesg if message.get_command() == '/start' else messages.help_mesg
        await bot.send_message(message.from_user.id, msg)

        try:
            await message.delete()
        except MessageCantBeDeleted:
            pass

    except CantInitiateConversation:
        await message.reply(messages.cant_initiate_conversation)
    except BotBlocked:
        await message.reply(messages.bot_blocked)
    except Unauthorized:
        await message.reply(messages.unauthorized)


def register_handlers_start(_dp: Dispatcher):
    _dp.register_message_handler(commands_start, commands=['start', 'help'], state=None)