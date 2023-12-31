from create_bot import dp, db_url
from aiogram.utils import executor

from DB import db_init
from handlers import register_handlers
from services import GoogleAPI


async def on_startup(_):
    await db_init(db_url)
    await GoogleAPI().init()
    register_handlers(dp)
    print("Бот запущен")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
