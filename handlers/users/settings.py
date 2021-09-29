from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import settings, filters, subscribes

from data.messages import settings_text, filters_text, subscribes_text

from loader import dp
from utils.db_api import User, session


@dp.message_handler(Command("settings"))
async def show_settings(message: Message):
    with session() as s:
        user = s.query(User).get(message.from_user.id)

        text = settings_text.format(await user.get_has_subscribes(), await user.get_has_filters())

    await message.answer(text, reply_markup=settings)


@dp.callback_query_handler(text="filters")
async def show_filters(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        text = filters_text.format(await user.filters.get_title(), await user.filters.get_description(), await user.filters.get_tags())

    await call.message.edit_text(text, reply_markup=filters)
    await call.answer()


@dp.callback_query_handler(text="subscribes")
async def show_subscribes(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        text = subscribes_text.format(await user.subscribes.get_weblancer(), await user.subscribes.get_habr())

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer()
