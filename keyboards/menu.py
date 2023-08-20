from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class InlineMenu:
    """
        Класс отображения клавиатур
    """
    menu_cd = CallbackData("show_menu", "level", "category")

    def make_callback_data(self, level, category=0):
        """
            Создание callback меню админа
        """
        return self.menu_cd.new(level=level, category=category)

    async def menu_keyboard(self):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Список разделов курса", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=1))
        )

        markup.row(
            InlineKeyboardButton(text="Список контрольных точек", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=2))
        )

        markup.row(
            InlineKeyboardButton(text="О курсе", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=3))
        )

        markup.row(
            InlineKeyboardButton(text="Расписание", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=4))
        )

        markup.row(
            InlineKeyboardButton(text="Задание дня", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=5))
        )

        markup.row(
            InlineKeyboardButton(text="База знаний", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=6))
        )

        markup.row(
            InlineKeyboardButton(text="О себе", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=7))
        )

        markup.row(
            InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=8))
        )

        return markup
