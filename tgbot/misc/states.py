from aiogram.dispatcher.filters.state import StatesGroup, State


class KeyWordsInput(StatesGroup):
    waiting_for_input = State()
