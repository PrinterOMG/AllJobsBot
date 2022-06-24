from aiogram.utils.exceptions import BotBlocked

from loader import weblancer_parser, habr_parser, bot
from data.messages import new_web_job_text, new_habr_job_text
from data.config import WEBLANCER_PAGES_COUNT
from utils.db_api import User, session
from keyboards.inline import update


async def send_jobs():
    web_jobs = await weblancer_parser.parse_jobs(WEBLANCER_PAGES_COUNT)
    habr_job = await habr_parser.parse_last_job()

    with session() as s:
        users = s.query(User).filter(not User.is_blocked).all()

        for user in users:
            if user.subscribes.weblancer_subscribe:
                new_web_job = await user.get_new_web_job(web_jobs)

                if new_web_job:
                    text = new_web_job_text.format(new_web_job.title, new_web_job.price, new_web_job.description,
                                                   new_web_job.requests_count, new_web_job.time, new_web_job.url)

                    try:
                        await bot.send_message(chat_id=user.id, text=text, reply_markup=update,
                                               disable_web_page_preview=True)
                    except BotBlocked:
                        user.is_blocked = True

            if user.subscribes.habr_subscribe:
                new_habr_job = await user.get_new_habr_job(habr_job)

                if new_habr_job:
                    text = new_habr_job_text.format(new_habr_job.title, new_habr_job.price, new_habr_job.description,
                                                    new_habr_job.requests_count, new_habr_job.date, new_habr_job.url)

                    try:
                        await bot.send_message(chat_id=user.id, text=text, reply_markup=update,
                                               disable_web_page_preview=True)
                    except BotBlocked:
                        user.is_blocked = True
