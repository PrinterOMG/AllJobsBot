from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from utils.db_api import Filter, Subscribe, User, LastJob
from loader import dp, session, users


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

    if not session.query(User).get(message.chat.id):
        user = User(id=message.chat.id)
        filters = Filter(user_id=message.chat.id)
        subscribes = Subscribe(user_id=message.chat.id)
        last_jobs = LastJob(user_id=message.chat.id)

        users[message.chat.id] = user
        session.add_all([user, filters, subscribes, last_jobs])
        session.commit()

    else:
        pass
