from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class CheckpointsMenu:
    """
        Класс отображения клавиатур checkpoints
    """
    menu_cd = CallbackData("checkpoints_menu", "level", "category", "item_id")

    def make_callback_data(self, level, category=0, item_id=0):
        """
            Создание callback меню checkpoints
        """
        return self.menu_cd.new(level=level, category=category, item_id=item_id)

    async def menu_keyboard(self, points):
        """
            Клавиатура уровень 0
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        for point in points:
            button_text = f"{point[1]}"
            callback_data = self.make_callback_data(level=current_level + 1, item_id=point[0])

            markup.row(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

        return markup

    async def choose_item(self, item_id):
        current_level = 1
        markup = InlineKeyboardMarkup()

        markup.insert(
            InlineKeyboardButton(text="Отправить на проверку",
                                 callback_data=self.make_callback_data(level=current_level + 1, category=1,
                                                                       item_id=item_id))
        )

        markup.insert(
            InlineKeyboardButton(text="Методика", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                        category=2, item_id=item_id))
        )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1))
        )

        return markup

    async def back_keyboard(self, item_id):
        current_level = 2
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     item_id=item_id))
        )

        return markup
