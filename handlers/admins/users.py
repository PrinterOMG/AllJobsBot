from aiogram import types

from utils.db_api import Filter, Subscribe, User, LastJob, Tutorial, session
from loader import dp
from keyboards.inline import get_users_keyboard


USERS_PER_PAGE = 15


@dp.callback_query_handler(text="show users")
async def send_users(call: types.CallbackQuery):
    with session() as s:
        users = s.query(User).limit(USERS_PER_PAGE).all()

        users_list = ""
        for user in users:
            users_list += f"{user.id}\t{await user.get_has_subscribes()}\t{await user.get_has_filters()}\n"


