from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.handlers.filters import show_filters
from tgbot.misc import callbacks
from tgbot.services.database.models import User


async def close_message(call: CallbackQuery):
    await call.message.delete()
    await call.answer()


async def reset_tutorial(call: CallbackQuery):
    db = call.bot.get('database')

    async with db.begin() as session:
        user = await session.get(User, call.from_user.id)
        user.tutorial.reset_tutorial()

    await call.answer('Теперь вы снова увидите подсказки!', show_alert=True)


async def cancel(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    match callback_data['to']:
        case 'filters': await show_filters(call)


def register_other(dp: Dispatcher):
    dp.register_callback_query_handler(close_message, callbacks.action.filter(name='close'), state='*')
    dp.register_callback_query_handler(reset_tutorial, callbacks.action.filter(name='reset_tutorial'))
    dp.register_callback_query_handler(cancel, callbacks.cancel.filter(), state='*')
