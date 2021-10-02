from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


update = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Обновить", callback_data="update")
        ]
    ]
)
