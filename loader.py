from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiohttp import ClientSession

from sqlalchemy.orm import Session, sessionmaker

from data import config
from utils.db_api import User, engine
from utils.parsers import WeblancerParser, HabrParser

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

weblancer_parser = WeblancerParser()
habr_parsers = HabrParser()

session = Session(bind=engine)

users = dict()
users_from_db = session.query(User).all()
for user in users_from_db:
    users[user.id] = user

print(users)
