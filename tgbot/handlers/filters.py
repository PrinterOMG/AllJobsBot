from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages, states, callbacks
from tgbot.services.database.models import User
from tgbot.services.utils import pretty_bool


async def show_filters(call: CallbackQuery):
    db = call.bot.get('database')

    async with db() as session:
        user = await session.get(User, call.from_user.id)

        if user.tutorial.show_filters:
            user.tutorial.show_filters = False
            await call.answer(messages.filters_tutorial, show_alert=True)
            await session.commit()

    await call.message.edit_text(
        text=messages.filters.format(status=user.has_filters, key_words=', '.join(user.filters.filter_words)),
        reply_markup=inline_keyboards.filters
    )
    await call.answer()


async def clear_filters(call: CallbackQuery):
    db = call.bot.get('database')

    async with db.begin() as session:
        user = await session.get(User, call.from_user.id)
        if not user.filters.filter_words:
            await call.answer()
            return
        user.filters.filter_words = []

    await show_filters(call)


async def switch_filters(call: CallbackQuery):
    db = call.bot.get('database')

    async with db.begin() as session:
        user = await session.get(User, call.from_user.id)
        user.settings.include_filters = not user.settings.include_filters

    await show_filters(call)


async def start_key_words_input(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(messages.key_words_input, reply_markup=inline_keyboards.get_cancel_keyboard('filters'))
    await states.KeyWordsInput.waiting_for_input.set()
    await state.update_data(main_call=call.to_python())
    await call.answer()


async def get_key_words(message: Message, state: FSMContext):
    db = message.bot.get('database')
    new_key_words = message.text.split(', ')

    await message.delete()

    async with state.proxy() as data:
        main_call = CallbackQuery(**data['main_call'])

    async with db.begin() as session:
        user = await session.get(User, message.from_user.id)
        user.filters.filter_words = new_key_words

    await state.finish()
    await show_filters(main_call)


def register_filters(dp: Dispatcher):
    dp.register_callback_query_handler(show_filters, callbacks.navigation.filter(to='filters'))
    dp.register_callback_query_handler(start_key_words_input, callbacks.action.filter(name='key_words', payload='input'))
    dp.register_message_handler(get_key_words, state=states.KeyWordsInput.waiting_for_input)
    dp.register_callback_query_handler(clear_filters, callbacks.action.filter(name='key_words', payload='clear'))
    dp.register_callback_query_handler(switch_filters, callbacks.action.filter(name='switch_filters'))
