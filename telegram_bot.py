from create_bot import dp
from aiogram.utils import executor
from handlers import (start, menu, register_schedule_handlers, register_info_handlers, register_topics_handlers,
                      register_personal_handlers, register_day_task_handlers, register_checkpoints_handlers,
                      register_knowledge_handlers)

start.register_handlers_start(dp)
menu.register_handlers_menu(dp)
register_schedule_handlers(dp)
register_personal_handlers(dp)
register_knowledge_handlers(dp)
register_day_task_handlers(dp)
register_checkpoints_handlers(dp)
register_topics_handlers(dp)
register_info_handlers(dp)


async def on_startup(_):
    print("Бот запущен")


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)