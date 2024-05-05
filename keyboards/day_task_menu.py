from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class DayTaskMenu:
    """
        Класс отображения клавиатур dayTask
    """
    menu_cd = CallbackData("dayTask_menu", "level")

    def make_callback_data(self, level):
        """
            Создание callback меню dayTask
        """
        return self.menu_cd.new(level=level)

    async def menu_keyboard(self):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        markup.insert(
            InlineKeyboardButton(text="Отправить на проверку",
                                 callback_data=self.make_callback_data(level=current_level + 1))
        )

        return markup
