from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class TeamsMenu:
    """
        Класс отображения клавиатур knowledge
    """
    menu_cd = CallbackData("teams_menu", "level", "category", "method_id", "team_id")

    def make_callback_data(self, level, category=0, method_id=0, team_id=0):
        """
            Создание callback меню knowledge
        """
        return self.menu_cd.new(level=level, category=category, method_id=method_id, team_id=team_id)

    async def menu_keyboard(self, flag, team_id=0):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()
        if flag:
            markup.row(
                InlineKeyboardButton(text="Создать группу", callback_data=self.make_callback_data(
                    level=current_level + 1,
                    category=1, method_id=1))
            )

            markup.row(
                InlineKeyboardButton(text="Вступить в группу", callback_data=self.make_callback_data(
                    level=current_level + 1,
                    category=1, method_id=2))
            )

        else:
            markup.row(
                InlineKeyboardButton(text="Учасники", callback_data=self.make_callback_data(
                    level=current_level + 1,
                    category=2, method_id=1,
                    team_id=team_id))
            )

            markup.row(
                InlineKeyboardButton(text="Покинуть группу", callback_data=self.make_callback_data(
                    level=current_level + 1,
                    category=2, method_id=2,
                    team_id=team_id))
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

    async def back_keyboard(self, category, level):
        current_level = level
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     category=category))
        )

        return markup
