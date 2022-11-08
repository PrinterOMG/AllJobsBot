from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


users_callback = CallbackData("users_page", "action")


def get_users_keyboard(is_first=True, is_last=False):
    if is_first:
        keyboard = [
            [
                InlineKeyboardButton(text=">>>", callback_data=users_callback.new(action="next"))
            ]
        ]
    elif is_last:
        keyboard = [
            [
                InlineKeyboardButton(text="<<<", callback_data=users_callback.new(action="prev"))
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="<<<", callback_data=users_callback.new(action="prev")),
                InlineKeyboardButton(text=">>>", callback_data=users_callback.new(action="next"))
            ]
        ]

    keyboard.append([InlineKeyboardButton(text="Вернуться", callback_data="admin")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
