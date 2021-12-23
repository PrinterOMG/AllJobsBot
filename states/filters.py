import asyncio

from aiogram.types import Message, ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from keyboards.inline import filters

from data.messages import filters_text
from loader import dp, bot
from utils.db_api import User, session


class FiltersInput(StatesGroup):
    filters = State()


@dp.message_handler(state=FiltersInput.filters)
async def get_filters(message: Message, state: FSMContext):
    change_object = (await state.get_data("object"))["object"]
    temp_msg_id = (await state.get_data("temp_msg_id"))["temp_msg_id"]
    settings_msg_id = (await state.get_data("settings_msg_id"))["settings_msg_id"]

    text = message.text
    text = ";".join(map(lambda x: x.strip(), text.split(",")))

    with session() as s:
        user = s.query(User).get(message.from_user.id)

        if change_object == "key_words":
            user.filters.key_words = text

        await user.filters.check()

        text = filters_text.format(await user.filters.get_keywords())

    await state.finish()

    await message.delete()
    await asyncio.sleep(0.1)

    await bot.delete_message(chat_id=message.from_user.id, message_id=temp_msg_id)

    await bot.edit_message_text(chat_id=message.from_user.id, message_id=settings_msg_id, text=text,
                                reply_markup=filters, parse_mode=ParseMode.MARKDOWN)
