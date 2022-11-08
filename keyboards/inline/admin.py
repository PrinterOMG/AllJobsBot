from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Пользователи", callback_data="show_users")
    ],
    [
        InlineKeyboardButton(text="Создать пост", callback_data="create post")
    ],
    [
        InlineKeyboardButton(text="Закрыть", callback_data="close")
    ]
])
