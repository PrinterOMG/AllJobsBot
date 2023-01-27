from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc import messages


async def command_start(message: Message):
    await message.reply(messages.hello.format(username=message.from_user.username))


async def command_settings(message: Message):
    await message.answer('Settings')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(command_settings, commands=['settings'])
