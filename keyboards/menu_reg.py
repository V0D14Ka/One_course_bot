from keyboards.menu import Menu
from keyboards.schedule_menu import ScheduleMenu
from keyboards.knowledge_menu import KnowledgeMenu
from keyboards.topics_menu import TopicsMenu
from keyboards.day_task_menu import DayTaskMenu
from keyboards.faq_menu import FAQMenu
from keyboards.personal_menu import PersonalMenu
from keyboards.teams_menu import TeamsMenu


class InlineMenu(object):
    _instance = None
    menu = Menu()
    schedule_menu = ScheduleMenu()
    knowledge_menu = KnowledgeMenu()
    topics_menu = TopicsMenu()
    day_task_menu = DayTaskMenu()
    faq_menu = FAQMenu()
    personal_menu = PersonalMenu()
    teams_menu = TeamsMenu()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InlineMenu, cls).__new__(cls)
        return cls._instance

