from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class FAQMenu:
    """
        Класс отображения клавиатур FAQ
    """
    menu_cd = CallbackData("faq_menu", "level")

    def make_callback_data(self, level):
        """
            Создание callback меню FAQ
        """
        return self.menu_cd.new(level=level)

    async def menu_keyboard(self):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Написать преподавателю", callback_data=self.make_callback_data(
                level=current_level + 1))
        )

        return markup

