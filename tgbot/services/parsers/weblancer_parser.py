import asyncio
import datetime

import aiohttp
from bs4 import BeautifulSoup, Tag

from tgbot.services.parsers.base_parser import Parser
from tgbot.services.parsers.models import WeblancerJob


class WeblancerParser(Parser):
    marketplace_name = 'Weblancer'
    marketplace_url = 'https://www.weblancer.net'
    jobs_list_url = 'https://www.weblancer.net/jobs'

    @classmethod
    async def parse_last_job(cls) -> WeblancerJob | None:
        async with aiohttp.ClientSession() as session:
            page = 1
            while page < 5:
                async with session.get(cls.jobs_list_url + f'?page={page}') as response:
                    if not response.ok:
                        return None
                    soup = BeautifulSoup(await response.text(), 'lxml')

                jobs = soup.find_all('div', class_='row click_container-link set_href')
                for job in jobs:
                    if job.find('span', class_='icon-flag fixed_icon'):
                        continue

                    job_url = cls.marketplace_url + job.find('div', class_='title').find('a')['href']
                    return await cls.parse_job_with_url(job_url)

    @classmethod
    async def parse_job_with_url(cls, url: str) -> WeblancerJob | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if not response.ok:
                    return None
                soup = BeautifulSoup(await response.text(), 'lxml')

        job_html = soup.find('main', class_='content')
        return cls._get_job_data(job_html, url)

    @classmethod
    def _get_job_data(cls, job_html: Tag, url: str) -> WeblancerJob:
        print(url)
        customer_name = job_html.find('span', class_='name').text.strip()

        title = job_html.find('h1').text.strip()
        title = title[:title.find('№') - 3]
        description = job_html.find('div', class_='col-12 text_field').find('p').text.strip()

        price_tag = job_html.find('span', class_='title amount')
        price = price_tag.text.strip() if price_tag else 'Договорная'

        views_count = job_html.find('div', class_='dot_divided').find_all('span')[-1].text.split()[0]

        date_str = job_html.find('div', class_='float-right text-muted hidden-xs-down').find('span')['title'].strip()
        date_str = date_str.split(maxsplit=1)[1]
        date = datetime.datetime.strptime(date_str, '%d.%m.%Y %H:%M')

        requests_html = job_html.find('div', class_='block-content text_field')
        if requests_html:
            requests_str = requests_html.find('span').text
            requests_count = requests_str.split()[0]
        else:
            requests_count = 0

        job = WeblancerJob(
            url=url,
            title=title,
            description=description,
            date=date,
            requests_count=int(requests_count),
            views_count=int(views_count),
            price=price,
            customer_name=customer_name
        )

        return job


if __name__ == '__main__':
    asyncio.run(WeblancerParser.parse_last_job())
