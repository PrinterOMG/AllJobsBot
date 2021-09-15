from loader import session, weblancer_parser, habr_parsers, users


async def send_jobs():
    web_jobs = await weblancer_parser.parse_jobs(2)
    habr_job = await habr_parsers.parse_last_job()

    for user in users.values():
        if user.subscribes.weblancer_subscribe:
            new_web_job = await user.get_new_web_job()


