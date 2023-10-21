from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class TopicsMenu:
    """
        Класс отображения клавиатур topics
    """
    menu_cd = CallbackData("topics_menu", "level", "chapter", "item_id", "theme", "category", "choose", "upload")

    def make_callback_data(self, level, chapter=0, item_id=0, theme=0, category=0, choose=-1, upload=0):
        """
            Создание callback меню topics
        """
        return self.menu_cd.new(level=level, chapter=chapter, item_id=item_id, theme=theme, category=category, choose=choose, upload=upload)

    async def menu_cp_keyboard(self, points):
        """
            Клавиатура уровень 0 checkpoints
        """
        markup = InlineKeyboardMarkup()

        for point in points:
            button_text = f"{point[1]}"
            markup.row(
                InlineKeyboardButton(text=button_text, callback_data=self.make_callback_data(level=2,
                                                                                      chapter=point[1],
                                                                                      category=2))
            )

        return markup

    async def menu_keyboard(self, chapters):
        """
            Клавиатура уровень 0 topics
        """

        current_level = 0
        markup = InlineKeyboardMarkup()

        for topic in chapters:
            button_text = f"{topic[1]}"
            callback_data = self.make_callback_data(level=current_level + 1, chapter=topic[1])

            markup.row(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

        return markup

    async def choose_category(self, chapter):
        current_level = 1
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Список тем к разделу", callback_data=self.make_callback_data(
                level=current_level + 1, chapter=chapter,
                category=1))
        )

        markup.row(
            InlineKeyboardButton(text="КТ", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                  chapter=chapter,
                                                                                  category=2))
        )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1))
        )

        return markup

    # Клавиатура для выбора темы уровень 2
    async def choose_theme(self, chapter, themes):
        current_level = 2
        markup = InlineKeyboardMarkup()

        for theme in themes:
            button_text = f"{theme[1]}"
            callback_data = self.make_callback_data(level=current_level + 1, chapter=chapter, theme=theme[0], category=1)

            markup.row(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     chapter=chapter))
        )

        return markup

    # Клавиатура для информации о КТ
    async def checkpoint_info(self, chapter, is_lead=0, info=True):
        current_level = 2
        markup = InlineKeyboardMarkup()

        if info:
            markup.row(
                InlineKeyboardButton(text="Методика", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                            chapter=chapter, category=2))
            )

            if is_lead:
                markup.row(
                    InlineKeyboardButton(text="Отправить на проверку", callback_data=self.make_callback_data(
                        level=current_level + 1,
                        chapter=chapter, category=2, upload=1))
                )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     chapter=chapter))
        )

        return markup

    async def theme_info(self, chapter, theme):
        current_level = 3
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Раздатка", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                        chapter=chapter, theme=theme,
                                                                                        category=1, choose=4))
        )

        markup.row(
            InlineKeyboardButton(text="ДЗ", callback_data=self.make_callback_data(level=current_level + 1,
                                                                                  chapter=chapter, theme=theme,
                                                                                  category=1, choose=0))
        )

        markup.row(
            InlineKeyboardButton(text="Опрос", callback_data=self.make_callback_data(
                level=current_level + 1,
                chapter=chapter, theme=theme,
                category=1, choose=3))
        )

        markup.row(
            InlineKeyboardButton(text="Ссылки", callback_data=self.make_callback_data(
                level=current_level + 1,
                chapter=chapter, theme=theme,
                category=1, choose=1))
        )

        markup.row(
            InlineKeyboardButton(text="Расписание", callback_data=self.make_callback_data(
                level=current_level + 1,
                chapter=chapter, theme=theme,
                category=1, choose=2))
        )

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     chapter=chapter, category=1))
        )

        return markup

    # Временная мера
    async def back_keyboard(self, chapter, theme, category, level):
        current_level = level
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton(text="Назад", callback_data=self.make_callback_data(level=current_level - 1,
                                                                                     chapter=chapter, theme=theme,
                                                                                     category=category))
        )

        return markup
