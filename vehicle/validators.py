import re
from rest_framework.serializers import ValidationError


class TitleValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """
        Регулярные выражения в программу курса не входят.
        Лектор упоминает регулярки, поскольку это может быть хорошим
        ешением задачи, но ее можно решить и без регулярок, используя знания
        python, полученные на курсах 1 и 2.

        Если ты хочешь составить регулярное выражение, я рекомендую ресурс
        https://regex101.com/ , он содержит всю необходимую информацию по
        синтаксису регулярных выражений и позволяет тестировать написанные
        регулярки на конкретных строках.
        """

        reg = re.compile('^[a-zA-Z0-9\.\-\ ]+$')  # регулярное выражение
        # ссылка на видео ютьюб (https://www.youtube.com/watch?v=8sv-6AN0_cg)

        # Так как value это словарь (ordering dict), то надо из него извлечь
        # то значение того поля, которое мы хотим валидировать
        tmp_val = dict(value).get(self.field)  # переводим ordering dict в
        # dict и пытаемся получить значение того поля, которое мы хотим
        # отвалидировать

        if not bool(reg.match(tmp_val)):
            raise ValidationError('Title is not ok')
