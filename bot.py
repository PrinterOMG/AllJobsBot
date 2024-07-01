import asyncio
import logging
import os
import datetime

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from tgbot.config import Settings
from tgbot import handlers
from tgbot import filters
from tgbot import middlewares
from tgbot.services.database.base import Base
from tgbot.services.parsers import parsers_dict
from tgbot.services.schedulers import start_schedulers

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, settings):
    dp.setup_middleware(middlewares.EnvironmentMiddleware(settings=settings))
    dp.setup_middleware(middlewares.ThrottlingMiddleware())


def register_all_filters(dp):
    for aiogram_filter in filters.filters:
        dp.filters_factory.bind(aiogram_filter)


def register_all_handlers(dp):
    for register in handlers.register_functions:
        register(dp)


async def main():
    log_file = rf'logs/{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.log'
    if not os.path.exists('logs'): os.mkdir('logs')
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        handlers=(logging.FileHandler(log_file), logging.StreamHandler())
    )
    logger.info('Starting bot')

    settings = Settings()

    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode='HTML')
    bot_info = await bot.me
    logger.info(f'Bot: {bot_info.username} [{bot_info.mention}]')

    storage = RedisStorage2(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    dp = Dispatcher(bot, storage=storage)
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    bot['settings'] = settings
    bot['redis'] = redis
    bot['database'] = AsyncSessionLocal

    register_all_middlewares(dp, settings)
    register_all_filters(dp)
    register_all_handlers(dp)

    logging.getLogger('schedule').propagate = False
    asyncio.create_task(start_schedulers(bot, settings, AsyncSessionLocal, redis, parsers_dict))

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()

        bot_session = await bot.get_session()
        await bot_session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        logger.error('Bot stopped!')
        raise e
