from bs4 import BeautifulSoup
from .parsers_helper import Job
from .core_parser import Parser


class WeblancerParser(Parser):
    def __init__(self, session):
        """
        Инициализация класса

        :param session: Сессия библиотеки Requests, через которую будут отправляться запросы
        """
        super().__init__(session)

        self.request_url = "https://www.weblancer.net/jobs/?page={0}"
        self.url = "https://www.weblancer.net"

    async def parse_jobs(self, pages_count: int) -> list:
        """
        Возвращает отфильтрованный список заказов

        :param pages_count: Количество страниц для парсинга
        :param filters: Фильтры для парсинга, по умолчанию None
        :return: Отфильтрованный список заказов
        """
        parsed_jobs = list()
        for page in range(1, pages_count + 1):
            url = self.request_url.format(page)

            response = await self.session.get(url)
            soup = BeautifulSoup(response.text, "lxml")

            jobs = soup.find_all("div", class_="row click_container-link set_href")

            for job in jobs:
                job = await self._get_job_data(job)

                if not job:
                    continue

                parsed_jobs.append(job)

        return parsed_jobs

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

        date = job.find("span", class_="time_ago")
        delta_time = date.text
        date = date["title"]

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
