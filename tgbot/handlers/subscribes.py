from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils import markdown as md

from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages, callbacks
from tgbot.services.database.models import User
from tgbot.services.parsers import parsers_dict
from tgbot.services.utils import pretty_bool


async def show_subscribes(call: CallbackQuery):
    db = call.bot.get('database')

    async with db() as session:
        user = await session.get(User, call.from_user.id)

    subscribes_iter = (messages.subscribe_line.format(marketplace=md.hcode(parser), status=pretty_bool(parser in user.settings.subscribes)) for parser in parsers_dict)
    text = messages.subscribes.format(subscribes_list='\n\n'.join(subscribes_iter))
    await call.message.edit_text(text, reply_markup=inline_keyboards.get_subscribes_keyboard())
    await call.answer()


async def switch_subscribe(call: CallbackQuery, callback_data: dict):
    marketplace = callback_data['payload']
    db = call.bot.get('database')

    async with db.begin() as session:
        user = await session.get(User, call.from_user.id)
        if marketplace is user.settings.subscribes:
            user.settings.subscribes.remove(marketplace)
        else:
            user.settings.subscribes.append(marketplace)

    await show_subscribes(call)


async def update_subscribes(call: CallbackQuery, callback_data: dict):
    action = callback_data['payload']
    new_value = [] if action == 'clear' else list(parsers_dict.keys())
    db = call.bot.get('database')

    async with db.begin() as session:
        user = await session.get(User, call.from_user.id)
        user.settings.subscribes = new_value

    await show_subscribes(call)


def register_subscribes(dp: Dispatcher):
    dp.register_callback_query_handler(show_subscribes, callbacks.navigation.filter(to='subscribes'))
    dp.register_callback_query_handler(switch_subscribe, callbacks.action.filter(name='switch_sub'))
    dp.register_callback_query_handler(update_subscribes, callbacks.action.filter(name='update_subs'))
