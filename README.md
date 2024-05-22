# One_course_bot


## Содержание

- [Установка](#установка)
- [GoogleAPI](#google)

## Установка <a name="установка"></a>

Установка и запуск проекта

```bash
git clone https://github.com/V0D14Ka/One_course_bot.git
cd One_course_bot
pip install -r requirements.txt
python telegram_bot.py
```

## GoogleAPI <a name="google"></a>
Ссылки на используемые таблицы:
  - [Разделы](https://docs.google.com/spreadsheets/d/1vHCGeH0nuCY7tbp-7eo4IbcjoXiXpoX2Sg2NLp6HVAY)
  - [Банк знаний](https://docs.google.com/spreadsheets/d/1UzMVOBYZPReVd74GWikXJncPWOvrRA0KzTspehdMNk0)
  - [FAQ](https://docs.google.com/spreadsheets/d/1DWoyVUyDYwDiXO2Tw-n_vweb0z5UE2WRaSODiOG6Eo4)
  - [Группы](https://docs.google.com/spreadsheets/d/1DWoyVUyDYwDiXO2Tw-n_vweb0z5UE2WRaSODiOG6Eo4)

Ссылки на Google Drive:
  - [Тестовая папка загрузки](https://drive.google.com/drive/u/1/folders/1KU8WOgqxc9LmVonxF2IEdT9bkYyQBqce)

Описание класса:
  - ```get_themes(chapter)``` - получение тем выбранного раздела.
  - ```get_theme_info(chapter, theme)``` - получение информации о выбранной теме.
  - ```get_checkpoint(chapter)``` - получение информации о выбранном чекпоинте.
  - ```get_knowledge(chapter)``` - получение методов базы знаний выбранного раздела
  - ```get_method_info(chapter, method_id)``` - получение материала по выбранному методу.
  - ```get_faq():``` - получение списка часто задаваемых вопросов.
  - ```get_lessons_dates(summary)``` - получение расписаний выбранных мероприятий.
  - ```get_period_lessons(period)``` - получение расписаний мероприятий за выбранный период.
  - ```check_user(group, full_name)``` - проверка наличия пользователя в группе.
  - ```set_id(tg_id, col, group)``` - устанавливает telegram_id студенту, после регистрации.