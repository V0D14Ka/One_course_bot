from aiogram import Dispatcher

from handlers.commands import checkpoints, topics, schedule, personal, day_task, knowledge, info


def register_commands_handlers(_dp: Dispatcher):
    _dp.register_message_handler(checkpoints, commands=['checkpoints'])
    _dp.register_message_handler(topics, commands=['topics'])
    _dp.register_message_handler(schedule, commands=['schedule'])
    _dp.register_message_handler(personal, commands=['personal'])
    _dp.register_message_handler(day_task, commands=['day_task'])
    _dp.register_message_handler(knowledge, commands=['knowledge'])
    _dp.register_message_handler(info, commands=['info'])

