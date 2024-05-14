from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class KnowledgeMenu:
    """
        Класс отображения клавиатур knowledge
    """
    menu_cd = CallbackData("knowledge_menu", "level", "category", "method_id")

    def make_callback_data(self, level, category=0, method_id=0):
        """
            Создание callback меню knowledge
        """
        return self.menu_cd.new(level=level, category=category, method_id=method_id)

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

    async def choose_method(self, category, methods):
        current_level = 1
        markup = InlineKeyboardMarkup()

        for topic in methods:
            button_text = f"{topic[1]}"
            callback_data = self.make_callback_data(level=current_level + 1, category=category, method_id=topic[0])

            markup.row(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     category=category))
        )

        return markup

    async def back_keyboard(self, category):
        current_level = 2
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     category=category))
        )

        return markup
