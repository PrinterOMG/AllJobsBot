from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import subscribes, subscribes_callback, settings
from data.messages import settings_text, subscribes_text

from loader import dp, users, session


@dp.callback_query_handler(subscribes_callback.filter(object="back"))
async def go_to_settings(call: CallbackQuery):
    user = users[call.from_user.id]

    text = settings_text.format(await user.get_has_subscribes(), await user.get_has_filters())

    await call.message.edit_text(text, reply_markup=settings)
    await call.answer()


@dp.callback_query_handler(subscribes_callback.filter(object="weblancer"))
async def change_weblancer_subscribe(call: CallbackQuery):
    user = users[call.from_user.id]

    user.subscribes.weblancer_subscribe = not user.subscribes.weblancer_subscribe
    await user.subscribes.check()

    text = subscribes_text.format(await user.subscribes.get_weblancer(), await user.subscribes.get_habr())

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer()

    session.commit()


@dp.callback_query_handler(subscribes_callback.filter(object="habr"))
async def change_habr_subscribe(call: CallbackQuery):
    user = users[call.from_user.id]

    user.subscribes.habr_subscribe = not user.subscribes.habr_subscribe
    await user.subscribes.check()

    text = subscribes_text.format(await user.subscribes.get_weblancer(), await user.subscribes.get_habr())

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer()

    session.commit()
