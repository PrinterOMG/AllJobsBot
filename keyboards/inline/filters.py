from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


filter_callback = CallbackData("filter", "action", "object")

filters = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить заголовки", callback_data=filter_callback.new(action="change", object="title")),
            InlineKeyboardButton(text="Очистить", callback_data=filter_callback.new(action="clear", object="title"))
        ],
        [
            InlineKeyboardButton(text="Изменить описание", callback_data=filter_callback.new(action="change", object="description")),
            InlineKeyboardButton(text="Очистить", callback_data=filter_callback.new(action="clear", object="description"))
        ],
        [
            InlineKeyboardButton(text="Изменить теги", callback_data=filter_callback.new(action="change", object="tags")),
            InlineKeyboardButton(text="Очистить", callback_data=filter_callback.new(action="clear", object="tags"))
        ],
        [
            InlineKeyboardButton(text="Изменить всё", callback_data=filter_callback.new(action="change", object="all")),
            InlineKeyboardButton(text="Очистить", callback_data=filter_callback.new(action="clear", object="all"))
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data=filter_callback.new(action="back", object="none"))
        ]
    ]
)
