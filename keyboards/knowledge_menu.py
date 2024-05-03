from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class KnowledgeMenu:
    """
        Класс отображения клавиатур knowledge
    """
    menu_cd = CallbackData("knowledge_menu", "level", "category")

    def make_callback_data(self, level, category=0):
        """
            Создание callback меню knowledge
        """
        return self.menu_cd.new(level=level, category=category)

    async def menu_keyboard(self):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Методики", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=1))
        )

        markup.row(
            InlineKeyboardButton(text="Маркетинг", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=2))
        )

        markup.row(
            InlineKeyboardButton(text="Заначка", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=3))
        )

        return markup

    async def back_keyboard(self):
        current_level = 1
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level-1))
        )

        return markup

