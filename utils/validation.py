import re


class Validation(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Validation, cls).__new__(cls)
        return cls._instance
    """
        Валидация на регулярных выражениях.
    """

    async def val_digit(self, amount):
        """
            Валидация положительное число.

            :param amount: Число.

            :return: 200 если все хорошо, иначе строку с ошибкой.
        """
        if not str(amount).replace('.', '').isdigit() or str(amount)[0] in "0,.-":
            return "Значение должно быть положительным числом!"
        if len(amount) > 10:
            return "Слишком длинное число"
        return 200


    async def val_fio(self, text):
        """
            Валидация ФИО.

            :param text: ФИО вида Иванов Иван Иванович.

            :return: 200 если все хорошо, иначе строку с ошибкой.
        """
        if len(text) > 70:
            return "Слишком большой ввод"
        pattern = re.compile("^[а-яА-ЯёЁa-zA-Z]+ [а-яА-ЯёЁa-zA-Z]+ ?[а-яА-ЯёЁa-zA-Z]+$")  # pattern
        return 200 if re.fullmatch(pattern, text) else "Неверный формат ввода ФИО"

    async def val_mix(self, string):
        """
            Валидация смеси текст + числа.

            :param string: Строка.

            :return: 200 если все хорошо, иначе строку с ошибкой.
        """
        if len(string) > 100:
            return "Слишком длинное значение"
        return 200