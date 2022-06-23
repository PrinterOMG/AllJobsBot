from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ParseMode

from keyboards.inline import settings, filters, subscribes

from data.messages import settings_text, filters_text, subscribes_text

from loader import dp, bot
from utils.db_api import User, session


@dp.message_handler(Command("settings"))
async def show_settings(message: Message):
    with session() as s:
        user = s.query(User).get(message.from_user.id)

        if user:
            text = settings_text.format(await user.get_has_subscribes(), await user.get_has_filters())
        else:
            await message.answer("Пожалуйста, напишите /start")

    await message.answer(text, reply_markup=settings)
    await message.delete()


@dp.callback_query_handler(text="filters")
async def show_filters(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        text = filters_text.format(await user.get_has_filters(), await user.filters.get_keywords())

    await call.message.edit_text(text, reply_markup=filters, parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()


@dp.callback_query_handler(text="subscribes")
async def show_subscribes(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        text = subscribes_text.format(await user.subscribes.get_weblancer(), await user.subscribes.get_habr())

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer()


@dp.callback_query_handler(text="close")
async def close_settings_message(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
