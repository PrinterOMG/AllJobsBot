import asyncio

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline import filters, filter_callback, settings

from data.messages import settings_text, filters_text
from loader import dp, bot
from utils.db_api import User, session


class FiltersInput(StatesGroup):
    filters = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('Отменено')


@dp.message_handler(state=FiltersInput.filters)
async def get_filters(message: Message, state: FSMContext):
    change_object = (await state.get_data("object"))["object"]
    temp_msg_id = (await state.get_data("temp_msg_id"))["temp_msg_id"]
    settings_msg_id = (await state.get_data("settings_msg_id"))["settings_msg_id"]

    text = message.text
    text = ";".join(map(lambda x: x.strip(), text.split(",")))

    with session() as s:
        user = s.query(User).get(message.from_user.id)

        if change_object == "title":
            user.filters.title = text

        elif change_object == "description":
            user.filters.description = text

        elif change_object == "tags":
            user.filters.tags = text

        elif change_object == "all":
            user.filters.title = text
            user.filters.description = text
            user.filters.tags = text

        await user.filters.check()

        text = filters_text.format(await user.filters.get_title(), await user.filters.get_description(),
                                   await user.filters.get_tags())

    await state.finish()

    await message.delete()
    await asyncio.sleep(0.1)

    await bot.delete_message(chat_id=message.from_user.id, message_id=temp_msg_id)

    await bot.edit_message_text(chat_id=message.from_user.id, message_id=settings_msg_id, text=text, reply_markup=filters)


@dp.callback_query_handler(filter_callback.filter(action="clear"))
async def clear_filter(call: CallbackQuery, callback_data: dict):
    clear_object = callback_data["object"]

    with session() as s:
        user = s.query(User).get(call.from_user.id)

        if clear_object == "all":
            await user.filters.clear_all()

        else:
            if clear_object == "title":
                user.filters.title = ""
            elif clear_object == "description":
                user.filters.description = ""
            elif clear_object == "tags":
                user.filters.tags = ""

            await user.filters.check()

        text = filters_text.format(await user.filters.get_title(), await user.filters.get_description(),
                                   await user.filters.get_tags())

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=filters)

    await call.answer("Успешно очищено!")


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

        text = settings_text.format(await user.get_has_subscribes(), await user.get_has_filters())

    await call.message.edit_text(text, reply_markup=settings)
    await call.answer()
