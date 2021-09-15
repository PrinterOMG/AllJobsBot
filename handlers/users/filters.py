from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline import filters, filter_callback, settings

from loader import dp, users, session


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
    user = users[message.chat.id]
    change_object = await state.get_state("object")

    text = message.text
    text = ";".join(map(lambda x: x.strip(), text.split(",")))

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

    session.commit()

    await state.finish()


@dp.callback_query_handler(filter_callback.filter(action="clear"))
async def clear_filter(call: CallbackQuery, callback_data: dict):
    clear_object = callback_data["object"]

    if clear_object == "all":
        print("clear all")

    else:
        print("clear " + clear_object)

    await call.answer("test")


@dp.callback_query_handler(filter_callback.filter(action="change"))
async def change_filter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    change_object = callback_data["object"]

    await call.message.answer("Введите ключевые слова для фильтров через запятую:")

    await state.update_data(object=change_object)
    await FiltersInput.filters.set()

    await call.answer()


@dp.callback_query_handler(filter_callback.filter(action="back"))
async def back(call: CallbackQuery):
    await call.message.edit_text("Настройки", reply_markup=settings)
    await call.answer()
