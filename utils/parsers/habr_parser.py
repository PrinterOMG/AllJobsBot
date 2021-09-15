from .parsers_helper import Job
from .core_parser import Parser

from bs4 import BeautifulSoup


class HabrParser(Parser):
    def __init__(self, session):
        super().__init__(session)

        self.url = "https://freelance.habr.com/user_rss_tasks/ObKACbYdFK5Jgjnz9KgE8g=="

    async def parse_last_job(self) -> Job:
        response = await self.session.get(self.url)

        soup = BeautifulSoup(response.text, "lxml")
        job = await soup.find("item")
        job = await self._get_job_data(job)

        return job

    async def _get_job_data(self, job) -> Job:
        title = job.find("title").text
        url = job.find("guid").text
        date = job.find("pubdate").text
        description = job.find("description").text

        job = Job(
            title=title,
            description=description,
            url=url,
            date=date,
            tags=[],
            time="",
            requests_count=None,
            price=None,
            category=None
        )

        return job
