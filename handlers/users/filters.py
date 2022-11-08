from aiogram.types import CallbackQuery, ParseMode
from aiogram.dispatcher import FSMContext

from keyboards.inline import filters, filter_callback, settings

from data.messages import settings_text, filters_text
from loader import dp, bot
from utils.db_api import User, session
from states.filters import FiltersInput


@dp.callback_query_handler(filter_callback.filter(action="clear"))
async def clear_filter(call: CallbackQuery, callback_data: dict):
    clear_object = callback_data["object"]

    with session() as s:
        user = s.query(User).get(call.from_user.id)

        if clear_object == "key_words":
            user.filters.key_words = ""
            await user.filters.check()

        text = filters_text.format(status=await user.get_has_filters(),
                                   key_words=await user.filters.get_keywords())

    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=filters, parse_mode=ParseMode.MARKDOWN_V2)

        await call.answer("Успешно очищено!")
    except Exception:
        await call.answer("Нечего очищать!")


@dp.callback_query_handler(filter_callback.filter(action="change"))
async def change_filter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    change_object = callback_data["object"]

    temp_message = await call.message.answer("Введите ключевые слова для фильтров через запятую:")

    await state.update_data(object=change_object, temp_msg_id=temp_message.message_id, settings_msg_id=call.message.message_id)
    await FiltersInput.filters.set()

    await call.answer()


@dp.callback_query_handler(filter_callback.filter(action="back"))
async def back(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        text = settings_text.format(subscribes_status=await user.get_has_subscribes(),
                                    filters_status=await user.get_has_filters())

    await call.message.edit_text(text, reply_markup=settings)
    await call.answer()


@dp.callback_query_handler(filter_callback.filter(action="switch"))
async def switch_filter_status(call: CallbackQuery):
    with session() as s:
        user = s.query(User).get(call.from_user.id)

        if not user.filters.key_words:
            await call.answer(show_alert=True, text="У вас нет ключевых слов!")
            return

        user.has_filters = not user.has_filters

        text = filters_text.format(status=await user.get_has_filters(),
                                   key_words=await user.filters.get_keywords())

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                reply_markup=filters, parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()
