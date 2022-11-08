from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ParseMode

from keyboards.inline import settings, filters, subscribes

from data.messages import settings_text, filters_text, subscribes_text
import data.tutorial as tut

from loader import dp, bot
from utils.db_api import User, session


@dp.message_handler(Command("settings"))
async def show_settings(message: Message):
    with session() as s:
        user = s.query(User).get(message.from_user.id)

        if user:
            text = settings_text.format(subscribes_status=await user.get_has_subscribes(),
                                        filters_status=await user.get_has_filters())
        else:
            await message.answer("Пожалуйста, напишите /start")

    await message.answer(text, reply_markup=settings)
    await message.delete()


@dp.callback_query_handler(text="filters")
async def show_filters(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        show_tutorial = user.tutorial.show_filters
        if show_tutorial:
            user.tutorial.show_filters = False

        text = filters_text.format(status=await user.get_has_filters(),
                                   key_words=await user.filters.get_keywords())

    await call.message.edit_text(text, reply_markup=filters, parse_mode=ParseMode.MARKDOWN_V2)

    if show_tutorial:
        await call.answer(tut.filters, show_alert=True)
    else:
        await call.answer()


@dp.callback_query_handler(text="subscribes")
async def show_subscribes(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        show_tutorial = user.tutorial.show_subscribes
        if show_tutorial:
            user.tutorial.show_subscribes = False

        text = subscribes_text.format(
            weblancer=await user.subscribes.get_weblancer(),
            habr=await user.subscribes.get_habr(),
            freelance=await user.subscribes.get_freelance()
        )

    await call.message.edit_text(text, reply_markup=subscribes)

    if show_tutorial:
        await call.answer(tut.subscribes, show_alert=True)
    else:
        await call.answer()
