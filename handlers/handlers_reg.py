from handlers.commands import (register_schedule_handlers, register_info_handlers, register_topics_handlers,
                               register_personal_handlers, register_day_task_handlers, register_checkpoints_handlers,
                               register_knowledge_handlers, register_faq_handlers, register_teams_handlers)

from handlers.menu import register_handlers_menu
from handlers.start import register_handlers_start


def register_handlers(dp):
    register_handlers_start(dp)
    register_handlers_menu(dp)
    register_schedule_handlers(dp)
    register_personal_handlers(dp)
    register_knowledge_handlers(dp)
    register_day_task_handlers(dp)
    register_checkpoints_handlers(dp)
    register_topics_handlers(dp)
    register_info_handlers(dp)
    register_faq_handlers(dp)
    register_teams_handlers(dp)
