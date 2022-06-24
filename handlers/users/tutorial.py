from aiogram.types import CallbackQuery

from loader import dp
from utils.db_api import User, session


@dp.callback_query_handler(text="tutorial")
async def reset_tutorial(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        await user.tutorial.reset_tutorial()

    await call.answer("Обучение успешно сброшено!")
