import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from keyboards import InlineMenu, ScheduleMenu, KnowledgeMenu, CheckpointsMenu, TopicsMenu

load_dotenv()

inline_menu = InlineMenu()
schedule_menu = ScheduleMenu()
knowledge_menu = KnowledgeMenu()
checkpoints_menu = CheckpointsMenu()
topics_menu = TopicsMenu()
storage = MemoryStorage()
# validation = Validation()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
