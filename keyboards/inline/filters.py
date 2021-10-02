from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


filter_callback = CallbackData("filter", "action", "object")

filters = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ключевые слова", callback_data=filter_callback.new(action="change", object="key_words")),
            InlineKeyboardButton(text="Очистить", callback_data=filter_callback.new(action="clear", object="key_words"))
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data=filter_callback.new(action="back", object="none"))
        ]
    ]
)
