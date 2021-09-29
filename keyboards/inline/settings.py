from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подписки", callback_data="subscribes")
        ],
        [
            InlineKeyboardButton(text="Фильтры", callback_data="filters")
        ],
        [
            InlineKeyboardButton(text="Закрыть", callback_data="close")
        ]
    ]
)
