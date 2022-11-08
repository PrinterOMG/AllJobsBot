start_text = """
Добро пожаловать в бот для расслыке новых заказов на площадке Weblancer!

Подписаться на рассылку можно в настройках!
"""

# TODO: текст написать
help_text = """

"""

settings_text = """
⚙️Настройки

Статус подписок: {subscribes_status}

Статус фильтров: {filters_status}
"""

new_web_job_text = """
Появился новый заказ на Weblancer!

―――――――――――――――――――       

Название: {title}

💰 Цена: {price}

Описание: {description}

Количество заявок: {requests_count}

⏳ Дата: {date}

🔗 URL: {url}

―――――――――――――――――――
"""

new_habr_job_text = """
Появился новый заказ на Habr!

―――――――――――――――――――

Название: {title}

💰 Цена: {price}

Описание: {description}

Количество откликов: {requests_count} 

⏳ Дата: {date}

🔗 URL: {url}

―――――――――――――――――――
"""

new_freelance_job_text = """
Появился новый заказ на Freelance!

―――――――――――――――――――

Название: {title}

💰 Цена: {price}

Срок: {time}

Фрагмент описания: {description}

Количество откликов: {requests_count} 

⏳ Дата: {date}

🔗 URL: {url}

―――――――――――――――――――
"""

filters_text = """
Статус фильтров: {status}
Ваши фильтры:

Ключевые слова: `{key_words}`
"""

subscribes_text = """
Ваши подписки:

Подписка на Weblancer: {weblancer}

Подписка на Habr: {habr}

Подписка на Freelance: {freelance}
"""

no_post_text = "Этот заказ был удален: {url}"

users_text = """
id\tПодписка\tФильтр
{users_list}
"""
