import asyncio
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup, Tag

from tgbot.services.parsers.base_parser import Parser
from tgbot.services.parsers.schemas import HabrJob


class HabrParser(Parser):
    marketplace_name = 'Habr'
    marketplace_url = 'https://freelance.habr.com'
    jobs_list_url = 'https://freelance.habr.com/tasks'

    @classmethod
    async def parse_last_job(cls) -> HabrJob | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.jobs_list_url) as response:
                if not response.ok:
                    return None
                soup = BeautifulSoup(await response.text(), 'lxml')

        first_job_url = soup.find('li', class_='content-list__item').find('a')['href']
        first_job_url = cls.marketplace_url + first_job_url

        return await cls.parse_job_with_url(first_job_url)

    @classmethod
    async def parse_job_with_url(cls, url: str) -> HabrJob | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if not response.ok:
                    return None
                soup = BeautifulSoup(await response.text(), 'lxml')

        job = soup.find('section', class_='column_wrap')

        return cls._get_job_data(job, url)

    @classmethod
    def _get_job_data(cls, job_html: Tag, url: str) -> HabrJob:
        title = job_html.find('h2').text.strip()
        title = ' '.join(title.split())
        price = job_html.find('div', class_='task__finance').text.strip()

        task_meta = job_html.find('div', class_='task__meta')

        date_str = task_meta.text[:task_meta.text.find('•')].strip()
        date = cls._convert_habr_date_to_datetime(date_str)

        counts = task_meta.find_all('span')
        requests_count, views_count = int(counts[0].text), int(counts[1].text)

        customer_html = job_html.find('div', class_='fullname').find('a')
        customer_name, customer_url = customer_html.text.strip(), cls.marketplace_url + customer_html['href']

        description = job_html.find('div', class_='task__description').text.strip()

        job = HabrJob(
            title=title,
            description=description,
            price=price,
            views_count=views_count,
            requests_count=requests_count,
            customer_name=customer_name,
            customer_url=customer_url,
            url=url,
            date=date
        )

        return job

    @classmethod
    def _convert_habr_date_to_datetime(cls, date_str: str) -> datetime:
        """
        date_str example: '26 января 2023, 15:48'
        """
        month_names = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12
        }

        day, month_str, year, time = date_str.replace(',', '').split()
        month = month_names[month_str]
        hours, minutes = map(int, time.split(':'))

        date = datetime(year=int(year), month=month, day=int(day), hour=hours, minute=minutes)

        return date


if __name__ == '__main__':
    # print(HabrParser._convert_habr_date_to_datetime('26 января 2023, 15:48'))
    r = asyncio.run(HabrParser.parse_last_job())
    print(r)
