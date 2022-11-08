from aiogram import types

from loader import dp
from data.config import ADMINS
from keyboards.inline import admin


@dp.message_handler(commands=['admin'])
async def send_admin_menu(message: types.Message):
    if str(message.from_id) not in ADMINS:
        return

    await message.answer(text="Админ меню", reply_markup=admin)
    await message.delete()


@dp.callback_query_handler(text="admin")
async def show_admin_menu(call: types.CallbackQuery):
    if str(call.from_user.id) not in ADMINS:
        return

    await call.message.edit_text(text="Админ меню", reply_markup=admin)
