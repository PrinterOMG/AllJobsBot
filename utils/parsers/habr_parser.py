import re

import aiohttp

from .parsers_helper import Job
from .core_parser import Parser

from bs4 import BeautifulSoup


class HabrParser(Parser):
    def __init__(self):
        self.main_url = "https://freelance.habr.com/tasks"
        self.url_to_job = "https://freelance.habr.com"

    async def parse_last_job(self) -> Job:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.main_url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")

                job_url = self.url_to_job + soup.find("li", class_="content-list__item").find("a")["href"]

            async with session.get(job_url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")

        job = soup.find("div", class_="task task_detail")
        job = await self._get_job_data(job, job_url)

        return job

    async def parse_job_from_url(self, job_url) -> Job:
        async with aiohttp.ClientSession() as session:
            async with session.get(job_url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")

        job = soup.find("div", class_="task task_detail")
        job = await self._get_job_data(job, job_url)

        return job

    @staticmethod
    async def _get_job_data(job, url) -> Job:
        title = job.find("h2", class_="task__title").text.strip().split()
        title = " ".join(title)
        description = job.find("div", class_="task__description").text.strip()
        # description = re.sub('<[^<]+?>', '', description).strip()

        finance = job.find("div", class_="task__finance")
        if finance.find("span", class_="negotiated_price"):
            price = "Договорная"
        else:
            price = finance.find("span", class_="count").text

        meta_data = job.find("div", class_="task__meta")
        date = meta_data.text
        date = date[:date.find("•")].strip()
        requests_count = meta_data.find("span", class_="count").text

        tags = list()
        tags_raw = job.find_all("a", class_="tags__item_link")
        for tag in tags_raw:
            tags.append(tag.text)

        job = Job(
            title=title,
            description=description,
            url=url,
            date=date,
            tags=tags,
            time="",
            requests_count=requests_count,
            price=price,
            category=None
        )

        return job
