from aiogram.types import CallbackQuery

from keyboards.inline import update
from data.messages import new_habr_job_text, new_web_job_text, no_post_text
from loader import dp, weblancer_parser, habr_parser


@dp.callback_query_handler(text="update")
async def update_job_message(call: CallbackQuery):
    text = call.message.text
    job_url = text[text.find("URL: ") + 5:text.find('-', text.find("URL: "))].strip()

    if "habr" in job_url:
        job = await habr_parser.parse_job_from_url(job_url)
        if job:
            text = new_habr_job_text.format(
                title=job.title,
                price=job.price,
                description=job.description,
                requests_count=job.requests_count,
                date=job.date,
                url=job.url
            )
        else:
            text = no_post_text.format(url=job_url)
    else:
        job = await weblancer_parser.parse_job_from_url(job_url)
        if job:
            text = new_web_job_text.format(
                title=job.title,
                price=job.price,
                description=job.description,
                requests_count=job.requests_count,
                date=job.date,
                url=job.url
            )
        else:
            text = no_post_text.format(url=job_url)

    try:
        await call.message.edit_text(text=text, reply_markup=update, disable_web_page_preview=True)
        await call.answer("Обновлено")
    except Exception:
        await call.answer("Изменений нет")
