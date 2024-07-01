import datetime

import aiohttp

from tgbot.services.parsers.base_parser import Parser
from tgbot.services.parsers.schemas import InDevelopmentError, KWorkJob


class KWorkParser(Parser):
    marketplace_name = 'KWork'
    marketplace_url = 'https://kwork.ru'
    job_url = 'https://kwork.ru/projects/{job_id}/view'
    jobs_list_url = 'https://kwork.ru/projects'
    api_payload = {
        'page': 1,
        'view': 0,
        'c': 'all'
    }

    @classmethod
    async def parse_last_job(cls) -> KWorkJob | None:
        async with aiohttp.ClientSession() as session:
            async with session.post(cls.jobs_list_url, data=cls.api_payload) as response:
                if not response.ok:
                    return None
                data = await response.json()
                return cls._collect_data_to_job(data)

    @classmethod
    def _collect_data_to_job(cls, data) -> KWorkJob | None:
        """
        Data example:
        Dict -> 'data' key -> 'wants' key
        {
          "id": 1990630,
          "lang": "ru",
          "name": "Доработать логотип",
          "description": "Доброго дня всем!\nУ нас есть лого в svg, нужно его сделать адаптивным для соц сетей и youtubе, сделать объёмным и анимированным с эффектом появления, дополнительно вырезать отдельно дом с листком, как лого без надписей, сколько будет стоимость работ?",
          "status": "active",
          "url": "/projects/1990630",
          "files": [
            {
              "name": "логотип (прозрачный фон).svg",
              "url": "https://kwork.ru/files/uploaded/b0/ba/0e/c972add305/%D0%BB%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF%20%28%D0%BF%D1%80%D0%BE%D0%B7%D1%80%D0%B0%D1%87%D0%BD%D1%8B%D0%B9%20%D1%84%D0%BE%D0%BD%29.svg"
            }
          ],
          "isActive": true,
          "isHigherPrice": true,
          "isSymbolRu": true,
          "categoryMinPrice": 500,
          "priceLimit": "1000.00",
          "possiblePriceLimit": 3000,
          "dateView": null,
          "dateExpire": "2023-03-24 12:49:22",
          "dateCreate": "2023-03-23 11:41:41",
          "dateExpireText": "24 марта 2023",
          "dateCreateText": "23 марта 2023",
          "kworkCount": "2",
          "projectReviewType": null,
          "getReviewCanChange": false,
          "timeLeft": "23 ч. 48 мин.",
          "turnover": 0,
          "isUserWant": false,
          "userId": 14548379,
          "userName": "zeleniymagazin",
          "userAvatar": "noprofilepicture.gif",
          "userAvatarSrcSet": "",
          "userBackground": "#ee7aae",
          "userIsOnline": true,
          "userBadges": [],
          "userActiveWants": 1,
          "userWants": "1",
          "userIsOtherActiveWants": false,
          "userWantsHiredPercent": "0",
          "userAlreadyWork": null,
          "currentUserReviewType": null,
          "categoryName": "Логотип и брендинг",
          "parentCategoryName": "Дизайн"
        }
        """
        if not data['success']:
            return None

        job_dict = data['data']['wants'][0]
        job = KWorkJob(
            url=cls.job_url.format(job_id=job_dict['id']),
            title=job_dict['name'],
            description=job_dict['description'],
            date=datetime.datetime.strptime(job_dict['date_create'], '%Y-%m-%d %H:%M:%S'),
            requests_count=job_dict['kwork_count'],
            price=job_dict['priceLimit'] + '₽',
            customer_name=job_dict['user']['username'],
            min_price=int(job_dict['getPriceThreshold']),
            max_price=int(job_dict['possiblePriceLimit']),
            customer_url=job_dict['wantUserGetProfileUrl'],
        )

        return job

    @classmethod
    async def parse_job_with_url(cls, url: str) -> KWorkJob | None:
        raise InDevelopmentError
