import logging

import aioredis
from aiogram import Bot
from sqlalchemy import select

from tgbot.keyboards import inline_keyboards
from tgbot.services.database.models import User


async def send_jobs(bot: Bot, parsers: dict, db, redis: aioredis):
    new_jobs = []
    for marketplace, parser in parsers.items():
        try:
            new_job = await parser.parse_last_job()
        except Exception as e:
            logging.error(f'Something wrong with {marketplace} parser: {str(e)}')
            raise e
            continue
        new_jobs.append(new_job)

    async with db.begin() as session:
        users = await session.execute(select(User).where())
        users = users.scalars().all()

    for user in users:
        for job in new_jobs:
            if job.marketplace not in user.settings.subscribes:
                continue

            marketplace_key = f'{user.telegram_id}:{job.marketplace}'
            saved_jobs = [elem.decode() for elem in await redis.lrange(marketplace_key, 0, -1)]

            if job.url in saved_jobs:
                continue

            if len(saved_jobs) >= 5:
                await redis.rpop(marketplace_key)

            await redis.lpush(marketplace_key, job.url)

            if user.settings.include_filters and not user.filters.filter_job(job):
                continue

            try:
                await bot.send_message(chat_id=user.telegram_id, text=str(job),
                                       reply_markup=inline_keyboards.get_job_keyboard(job.url),
                                       disable_web_page_preview=True)
            except Exception as e:
                logging.error(f'Something wrong with user {user.telegram_id}: {e}')
