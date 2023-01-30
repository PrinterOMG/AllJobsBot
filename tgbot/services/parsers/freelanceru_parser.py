import asyncio
import datetime

import aiohttp
from bs4 import BeautifulSoup, Tag

from tgbot.services.parsers.base_parser import Parser
from tgbot.services.parsers.schemas import FreelanceRuJob, InDevelopmentError


class FreelanceRuParser(Parser):
    marketplace_name = 'FreelanceRu'
    marketplace_url = 'https://freelance.ru'
    jobs_list_url = 'https://freelance.ru/project/search'

    @classmethod
    async def parse_last_job(cls) -> FreelanceRuJob | None:
        async with aiohttp.ClientSession() as session:
            page = 1
            while page < 5:
                async with session.get(cls.jobs_list_url + f'?page={page}') as response:
                    if not response.ok:
                        return None
                    soup = BeautifulSoup(await response.text(), 'lxml')

                jobs = soup.find_all('div', class_='project')
                for job in jobs:
                    if job.find('img', class_='up'):
                        continue

                    job_url = cls.marketplace_url + job.find('a')['href']
                    return cls._get_job_data(job, job_url)

                page += 1

    @classmethod
    async def parse_job_with_url(cls, url: str) -> FreelanceRuJob | None:
        raise InDevelopmentError

    @classmethod
    def _get_job_data(cls, job_html: Tag, url: str) -> FreelanceRuJob:
        title = job_html.find('h2').text.strip()
        description = job_html.find('a', class_='description').text.strip()
        price = job_html.find('div', class_='cost').text.strip()
        term = job_html.find('div', class_='term').text.strip()
        customer_name = job_html.find('span', class_='user-name').text.strip()

        views_html = job_html.find('span', class_='view-count')
        views_count = int(views_html.text.strip()) if views_html else 0

        requests_html = job_html.find('span', class_='comments-count')
        requests_count = int(requests_html.text.strip()) if requests_html else 0

        is_premium = bool(job_html.find('div', class_='for-business'))

        date_str = job_html.find('div', class_='publish-time')['title'].replace('в ', '')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')

        job = FreelanceRuJob(
            url=url,
            title=title,
            description=description,
            date=date,
            requests_count=requests_count,
            price=price,
            customer_name=customer_name,
            views_count=views_count,
            term=term,
            is_premium=is_premium
        )

        return job


if __name__ == '__main__':
    print(asyncio.run(FreelanceRuParser.parse_last_job()))
