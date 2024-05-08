from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class PersonalMenu:
    """
        Класс отображения клавиатур PersonalMenu
    """
    menu_cd = CallbackData("personal_menu", "level", "category", "change")

    def make_callback_data(self, level, category=0, change=0):
        """
            Создание callback меню PersonalMenu
        """
        return self.menu_cd.new(level=level, category=category, change=change)

    async def menu_keyboard(self, flag):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Изменить" if flag else "Заполнить", callback_data=self.make_callback_data(
                level=current_level + 1,
                category=1 if flag else 2))
        )

        return markup

    async def to_change_keyboard(self):
        current_level = 1
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="ФИО", callback_data=self.make_callback_data(level=current_level + 1, change=1))
        )

        markup.row(
            InlineKeyboardButton(text="Номер курса", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                           change=2))
        )

        markup.row(
            InlineKeyboardButton(text="Номер группы", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                            change=3))
        )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1))
        )

        return markup

    async def back_keyboard(self):
        current_level = 1
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level-1))
        )

        return markup

