from aiogram.types import CallbackQuery

from keyboards.inline import subscribes, subscribes_callback, settings
from data.messages import settings_text, subscribes_text

from loader import dp
from utils.db_api import User, session


@dp.callback_query_handler(subscribes_callback.filter(object="back"))
async def go_to_settings(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)
        text = settings_text.format(await user.get_has_subscribes(), await user.get_has_filters())

    await call.message.edit_text(text, reply_markup=settings)
    await call.answer()


@dp.callback_query_handler(subscribes_callback.filter(object="weblancer"))
async def change_weblancer_subscribe(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)
        user.subscribes.weblancer_subscribe = not user.subscribes.weblancer_subscribe
        await user.subscribes.check()

        text = subscribes_text.format(
            weblancer=await user.subscribes.get_weblancer(),
            habr=await user.subscribes.get_habr(),
            freelance=await user.subscribes.get_freelance()
        )

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer("Успешно")


@dp.callback_query_handler(subscribes_callback.filter(object="freelance"))
async def change_freelance_subscribe(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)
        user.subscribes.freelance_subscribe = not user.subscribes.freelance_subscribe
        await user.subscribes.check()

        text = subscribes_text.format(
            weblancer=await user.subscribes.get_weblancer(),
            habr=await user.subscribes.get_habr(),
            freelance=await user.subscribes.get_freelance()
        )

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer("Успешно")



@dp.callback_query_handler(subscribes_callback.filter(object="habr"))
async def change_habr_subscribe(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        user.subscribes.habr_subscribe = not user.subscribes.habr_subscribe
        await user.subscribes.check()

        text = subscribes_text.format(
            weblancer=await user.subscribes.get_weblancer(),
            habr=await user.subscribes.get_habr(),
            freelance=await user.subscribes.get_freelance()
        )

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer("Успешно")


@dp.callback_query_handler(subscribes_callback.filter(object="sub_all"))
async def sub_all(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        await user.subscribes.sub_all()

        text = subscribes_text.format(
            weblancer=await user.subscribes.get_weblancer(),
            habr=await user.subscribes.get_habr(),
            freelance=await user.subscribes.get_freelance()
        )

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer("Успешно")


@dp.callback_query_handler(subscribes_callback.filter(object="unsub_all"))
async def sub_all(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        await user.subscribes.unsub_all()

        text = subscribes_text.format(
            weblancer=await user.subscribes.get_weblancer(),
            habr=await user.subscribes.get_habr(),
            freelance=await user.subscribes.get_freelance()
        )

    await call.message.edit_text(text, reply_markup=subscribes)
    await call.answer("Успешно")
