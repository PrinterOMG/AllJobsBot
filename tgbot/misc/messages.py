from aiogram.utils import markdown as md

hello = (
    'Hello, {username}'
)

settings = (
    '⚙️Настройки\n\n'
    'Статус подписок: {has_subscribes}\n'
    'Статус фильтров: {has_filters}'
)

subscribes = (
    'Ваши подписки:\n\n\n'
    '{subscribes_list}'
)
subscribe_line = 'Подписка на {marketplace}: {status}'

filters = (
    'Статус фильтров: {status}\n\n'
    f'{md.hbold("Ключевые слова: ")} {md.hcode("{key_words}")}'
)

key_words_input = (
    'Введите ключевые слова через запятую с пробелом\n'
    'Пример: "парсинг, бот, скрапинг"'
)
