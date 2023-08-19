import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from keyboards.menu import InlineMenu


load_dotenv()

inline_menu = InlineMenu()
storage = MemoryStorage()
# validation = Validation()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
