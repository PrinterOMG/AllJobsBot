import asyncio

import aioschedule
from aiogram import Bot

from tgbot.config import Config
from tgbot.services.schedulers.send_jobs import send_jobs


async def start_schedulers(bot: Bot, config: Config, db, redis, parsers):
    aioschedule.every(10).seconds.do(send_jobs, bot, parsers, db, redis)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
