import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from services.google_api import GoogleAPI
from utils import Validation

from keyboards import (InlineMenu, ScheduleMenu, KnowledgeMenu, TopicsMenu, DayTaskMenu, FAQMenu,
                       PersonalMenu, TeamsMenu)

load_dotenv()

inline_menu = InlineMenu()
schedule_menu = ScheduleMenu()
knowledge_menu = KnowledgeMenu()
topics_menu = TopicsMenu()
day_task_menu = DayTaskMenu()
faq_menu = FAQMenu()
personal_menu = PersonalMenu()
teams_menu = TeamsMenu()

google_api = GoogleAPI()
validation = Validation()

storage = MemoryStorage()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
