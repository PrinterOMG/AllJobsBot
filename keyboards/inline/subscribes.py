from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


subscribes_callback = CallbackData("change_subscribe", "object")

subscribes = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить статус подписки Weblancer", callback_data=subscribes_callback.new(object="weblancer"))
        ],
        [
            InlineKeyboardButton(text="Изменить статус подписки Habr", callback_data=subscribes_callback.new(object="habr"))
        ],
        [
            InlineKeyboardButton(text="Изменить статус подписки Freelance", callback_data=subscribes_callback.new(object="freelance"))
        ],
        [
            InlineKeyboardButton(text="Подписка на всё", callback_data=subscribes_callback.new(object="sub_all")),
            InlineKeyboardButton(text="Отписка от всего", callback_data=subscribes_callback.new(object="unsub_all"))
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data=subscribes_callback.new(object="back"))
        ]
    ]
)
