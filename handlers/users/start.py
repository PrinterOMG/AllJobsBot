from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from utils.db_api import Filter, Subscribe, User, LastJob, Tutorial, session
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

    with session() as s:
        if not s.query(User).get(message.chat.id):
            user = User()
            user.id = message.from_user.id

            filters = Filter()
            filters.user_id = message.from_user.id

            subscribes = Subscribe()
            subscribes.user_id = message.from_user.id

            last_jobs = LastJob()
            last_jobs.user_id = message.from_user.id

            tutorial = Tutorial()
            tutorial.user_id = message.from_user.id

            s.add_all([user, filters, subscribes, last_jobs, tutorial])
