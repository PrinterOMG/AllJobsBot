from aiogram.utils.exceptions import BotBlocked

from loader import weblancer_parser, habr_parser, freelance_parser, bot
from data.messages import new_web_job_text, new_habr_job_text, new_freelance_job_text
from utils.db_api import User, session
from keyboards.inline import update


async def send_jobs():
    web_job = await weblancer_parser.parse_last_job()
    habr_job = await habr_parser.parse_last_job()
    freelance_job = await freelance_parser.parse_last_job()

    with session() as s:
        users = s.query(User).filter(User.is_blocked == False).all()

        for user in users:
            if user.subscribes.weblancer_subscribe:
                new_web_job = await user.get_new_web_job(web_job)

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

            if user.subscribes.freelance_subscribe:
                new_freelance_job = await user.get_new_freelance_job(freelance_job)

                if new_freelance_job:
                    text = new_freelance_job_text.format(
                        title=new_freelance_job.title,
                        description=new_freelance_job.description,
                        price=new_freelance_job.price,
                        time=new_freelance_job.time,
                        requests_count=new_freelance_job.requests_count,
                        date=new_freelance_job.date,
                        url=new_freelance_job.url
                    )

                    try:
                        await bot.send_message(chat_id=user.id, text=text,
                                               disable_web_page_preview=True)
                    except BotBlocked:
                        user.is_blocked = True
