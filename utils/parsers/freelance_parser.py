import asyncio

import aiohttp
from bs4 import BeautifulSoup

from .parsers_helper import Job
from .core_parser import Parser


class FreelanceParser(Parser):
    url = "https://freelance.ru/project/search?page={page}"

    async def parse_last_job(self) -> Job:
        page = 1

        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url.format(page=page)) as response:
                    soup = BeautifulSoup(await response.text(), "lxml")

                jobs = soup.find_all("div", class_="box-shadow project")
                for job in jobs:
                    if job.find("i", class_="fa fa-angle-double-up"):
                        continue
                    if job.find("img", class_="fire"):
                        continue

                    last_job = await self._get_job_data(job)

                    return last_job
                else:
                    page += 1

    @staticmethod
    async def _get_job_data(job_raw) -> Job:
        job_data = {
            "title": "",
            "description": "",
            "url": "",
            "price": "",
            "category": "",
            "tags": [],
            "date": "",
            "time": "",
            "requests_count": 0
        }

        job_info_raw = job_raw.find("div", class_="box-title")
        job_conditions_raw = job_raw.find("div", class_="box-info")

        title_raw = job_info_raw.find("h2", class_="title").find("a")
        job_data["title"] = title_raw.text.strip()
        job_data["url"] = "https://freelance.ru" + title_raw["href"]

        job_data["description"] = job_info_raw.find("a", class_="description").text.strip()

        job_data["date"] = job_info_raw.find("time", class_="timeago").text.strip()

        requests_count_raw = job_info_raw.find("span", title="Отклики")
        if requests_count_raw:
            requests_count = requests_count_raw.text
            requests_count = int(requests_count[requests_count.rfind(":") + 1:])
        else:
            requests_count = 0
        job_data["requests_count"] = requests_count

        tags_raw = job_info_raw.find("span", class_="specs-list").find_all("span")
        tags = [tag.text.strip() for tag in tags_raw if "+" not in tag.text]
        job_data["tags"] = tags

        job_data["price"] = job_conditions_raw.find("div", class_="cost").text.strip()

        time_raw = job_conditions_raw.find("div", class_="term").text
        time = time_raw[time_raw.find(":") + 1:].strip()
        job_data["time"] = time

        if job_conditions_raw.find("li", class_="for-business text-success"):
            job_data["title"] += " (ПРЕМИУМ)"

        return Job(**job_data)


if __name__ == "__main__":
    job = asyncio.run(FreelanceParser().parse_last_job())
    print(job.title)
    print(job.description)
    print(job.url)
    print(job.price)
    print(job.time)
    print(job.date)
    print(job.tags)
