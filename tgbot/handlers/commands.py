from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages, callbacks
from tgbot.services.database.models import User, Settings, Filter, Tutorial


async def command_start(message: Message):
    db = message.bot.get('database')
    async with db.begin() as session:
        user = await session.get(User, message.from_id)
        if not user:
            new_user = User(telegram_id=message.from_id, settings=Settings(), filters=Filter(), tutorial=Tutorial())
            session.add(new_user)

    await message.reply(messages.hello.format(username=message.from_user.username))


async def command_settings(message: Message):
    db = message.bot.get('database')

    async with db() as session:
        user = await session.get(User, message.from_id)

    await message.delete()
    await message.answer(messages.settings.format(has_filters=user.has_filters, has_subscribes=user.has_subscribes),
                         reply_markup=inline_keyboards.settings)


async def show_settings(call: CallbackQuery):
    db = call.bot.get('database')

    async with db() as session:
        user = await session.get(User, call.from_user.id)

    await call.message.edit_text(
        messages.settings.format(has_filters=user.has_filters, has_subscribes=user.has_subscribes),
        reply_markup=inline_keyboards.settings
    )


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')

    dp.register_message_handler(command_settings, commands=['settings'])
    dp.register_callback_query_handler(show_settings, callbacks.navigation.filter(to='settings'))
