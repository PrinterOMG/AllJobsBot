from bs4 import BeautifulSoup
import aiohttp

from .parsers_helper import Job
from .core_parser import Parser


class WeblancerParser(Parser):
    def __init__(self):
        """
        Инициализация класса
        """

        self.request_url = "https://www.weblancer.net/jobs/?page={0}"
        self.url = "https://www.weblancer.net"

    async def parse_last_job(self) -> Job:
        """
        Возвращает отфильтрованный список заказов

        :return: Последний заказ
        """
        page = 1
        while True:
            url = self.request_url.format(page)

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soup = BeautifulSoup(await response.text(), "lxml")

            jobs = soup.find_all("div", class_="row click_container-link set_href")

            for job in jobs:
                job = await self._get_job_data(job)

                if job:
                    return job

            page += 1

    async def parse_job_from_url(self, job_url) -> Job | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(job_url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")
                page_ok = response.ok

        if not page_ok:
            return None
        title = soup.find("h1").text
        title = title[:title.rfind("–") - 1]

        description = soup.find("div", class_="cols_table no_hover").find("p").text.strip()

        time = soup.find("div", class_="float-right text-muted hidden-xs-down").find("span").text

        requests_count = soup.find("div", class_="block-content text_field").find("span").text.lower()
        if "нет" in requests_count:
            requests_count = 0
        else:
            requests_count = requests_count[:requests_count.find(" ")]

        if price := soup.find("span", class_="title amount"):
            price = price.text
        else:
            price = "Не указана"

        job = Job(
            title=title,
            price=price,
            url=job_url,
            description=description,
            category=None,
            tags=None,
            time=time,
            date=None,
            requests_count=requests_count
        )

        return job

    async def _get_job_data(self, job):
        """
        Возвращает словарь с данными о заказе

        :param job: Заказ, из которого будут собраны данные
        :return: Словарь с данными о заказе
        """

        if job.find("span", class_="icon-flag fixed_icon"):
            return None

        title_raw = job.find("a", class_="text-bold click_target show_visited")
        title = title_raw.text
        job_url = self.url + title_raw["href"]

        section = job.find("span", class_="text-nowrap").find("a").text

        tags_parent_raw = job.find("span", class_="d-flex flex-wrap")

        tags = list()
        if tags_parent_raw:
            tags_raw = tags_parent_raw.find_all("a")

            for tag_raw in tags_raw:
                tag = tag_raw.text.lower()
                tags.append(tag)

        text_raw = job.find("div", class_="text_field text-inline")

        price_raw = job.find("div", class_="float-right float-sm-none title amount indent-xs-b0").find("span")
        if price_raw:
            price = price_raw.text
        else:
            price = "Не указана"

        if text_raw.text:
            text = text_raw.text
        else:
            text = text_raw.find("div", class_="collapse").text

        if "Читать дальше" in text:
            text = text[text.find("Читать дальше"):].replace("Читать дальше", "").replace("Свернуть", "")

        if job.find("div", class_="text-muted", string="нет заявок"):
            requests_count = "0 заявок"
        else:
            requests_count = job.find("div", class_="float-left float-sm-none text_field").text.strip()

        date = job.find("span", class_="text-muted")
        delta_time = date.text
        date = (date.find("span"))["title"]

        job = Job(
            title=title,
            price=price,
            url=job_url,
            description=text,
            category=section,
            tags=tags,
            time=delta_time,
            date=date,
            requests_count=requests_count
        )

        return job
