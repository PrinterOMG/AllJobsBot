from datetime import datetime, timedelta

from pydantic import BaseModel


class Job(BaseModel):
    url: str
    title: str
    description: str
    date: datetime
    requests_count: int
    price: str
    customer_name: str

    marketplace: str
    marketplace_url: str


class HabrJob(Job):
    views_count: int
    customer_url: str

    marketplace = 'Habr'
    marketplace_url = 'https://freelance.habr.com/'


class FreelanceRuJob(Job):
    views_count: int
    term: timedelta
    is_premium: bool

    marketplace = 'FreelanceRu'
    marketplace_url = 'https://freelance.ru/'


class WeblancerJob(Job):
    views_count: int

    marketplace = 'Weblancer'
    marketplace_url = 'https://www.weblancer.net/'

