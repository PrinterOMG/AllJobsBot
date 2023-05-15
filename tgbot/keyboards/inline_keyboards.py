from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc import callbacks
from tgbot.services.database.models import User
from tgbot.services.parsers import parsers_dict
from tgbot.services.utils import pretty_bool

settings = InlineKeyboardMarkup(row_width=1)
settings.add(
    InlineKeyboardButton('Подписки', callback_data=callbacks.navigation.new('subscribes', '')),
    InlineKeyboardButton('Фильтры', callback_data=callbacks.navigation.new('filters', '')),
    InlineKeyboardButton('Сбросить обучение', callback_data=callbacks.action.new('reset_tutorial', '')),
    InlineKeyboardButton('Закрыть', callback_data=callbacks.action.new('close', ''))
)

filters = InlineKeyboardMarkup(row_width=2)
filters.add(
    InlineKeyboardButton('Ключевые слова', callback_data=callbacks.action.new('key_words', 'input')),
    InlineKeyboardButton('Очистить', callback_data=callbacks.action.new('key_words', 'clear'))
)
filters.add(
    InlineKeyboardButton('Вкл/выкл фильтры', callback_data=callbacks.action.new('switch_filters', ''))
)
filters.add(
    InlineKeyboardButton('Назад', callback_data=callbacks.navigation.new('settings', 'back'))
)


def get_cancel_keyboard(to, payload=''):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Отмена', callback_data=callbacks.cancel.new(to=to, payload=payload))
    )

    return keyboard


def get_job_keyboard(job_url):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('🌐 Открыть', url=job_url)
    )

    return keyboard


def get_subscribes_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = list()
    for marketplace in parsers_dict:
        buttons.append(
            InlineKeyboardButton(f'{marketplace}', callback_data=callbacks.action.new('switch_sub', marketplace))
        )
    keyboard.add(*buttons)

    keyboard.add(
        InlineKeyboardButton('Подписка на всё', callback_data=callbacks.action.new('update_subs', 'all')),
        InlineKeyboardButton('Отписка от всего', callback_data=callbacks.action.new('update_subs', 'clear')),
        InlineKeyboardButton('Назад', callback_data=callbacks.navigation.new('settings', 'back'))
    )

    return keyboard
