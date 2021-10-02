from aiogram.types import CallbackQuery

from keyboards.inline import update
from data.messages import new_habr_job_text, new_web_job_text
from loader import dp, weblancer_parser, habr_parser


@dp.callback_query_handler(text="update")
async def update_job_message(call: CallbackQuery):
    text = call.message.text
    job_url = text[text.find("URL: ") + 5:]

    if "habr" in job_url:
        job = await habr_parser.parse_job_from_url(job_url)
        text = new_habr_job_text.format(job.title, job.description, job.date, job.price, job.requests_count, job.url)

    else:
        job = await weblancer_parser.parse_job_from_url(job_url)
        text = new_web_job_text.format(job.title, job.price, job.description, job.requests_count, job.time, job.url)

    try:
        await call.message.edit_text(text=text, reply_markup=update)
        await call.answer("Обновлено")
    except Exception:
        await call.answer("Изменений нет")
