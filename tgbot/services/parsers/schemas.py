from datetime import datetime, timedelta

from aiogram.utils import markdown as md
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
    customer_url: str
    views_count: int

    marketplace: str = 'Habr'
    marketplace_url: str = 'https://freelance.habr.com/'

    def __str__(self):
        text = (
            f'Появился новый заказ на {self.marketplace}!\n\n'
            '―――――――――――――――――――\n\n'
            f'Название: {self.title}\n\n'
            f'Заказчик: {md.hlink(self.customer_name, self.customer_url)}\n\n'
            f'💰 Цена: {self.price}\n\n'
            f'Описание: {self.description}\n\n'
            f'Количество откликов: {self.requests_count}\n\n'
            f'Количество просмотров: {self.views_count}\n\n'
            f'⏳ Дата: {self.date}\n\n'
            '―――――――――――――――――――'
        )

        return text


class FreelanceRuJob(Job):
    term: str
    is_premium: bool
    views_count: int

    marketplace: str = 'FreelanceRu'
    marketplace_url: str = 'https://freelance.ru/'

    def __str__(self):
        premium_str = '⭐ Премиум ⭐\n' if self.is_premium else ""
        text = (
            f'Появился новый заказ на {self.marketplace}!\n\n'
            '―――――――――――――――――――\n\n'
            f'{premium_str}'
            f'Название: {self.title}\n\n'
            f'Заказчик: {self.customer_name}\n\n'
            f'💰 Цена: {self.price}\n\n'
            f'Описание: {self.description}\n\n'
            f'Количество откликов: {self.requests_count}\n\n'
            f'Количество просмотров: {self.views_count}\n\n'
            f'⏳ Дата: {self.date}\n'
            f'Срок: {self.term}\n\n'
            '―――――――――――――――――――'
        )

        return text


class WeblancerJob(Job):
    views_count: int

    marketplace: str = 'Weblancer'
    marketplace_url: str = 'https://www.weblancer.net/'

    def __str__(self):
        text = (
            f'Появился новый заказ на {self.marketplace}!\n\n'
            '―――――――――――――――――――\n\n'
            f'Название: {self.title}\n\n'
            f'Заказчик: {self.customer_name}\n\n'
            f'💰 Цена: {self.price}\n\n'
            f'Описание: {self.description}\n\n'
            f'Количество откликов: {self.requests_count}\n\n'
            f'Количество просмотров: {self.views_count}\n\n'
            f'⏳ Дата: {self.date}\n\n'
            '―――――――――――――――――――'
        )

        return text


class KWorkJob(Job):
    expire_date: datetime
    min_price: int
    max_price: int
    customer_url: str

    marketplace: str = 'KWork'
    marketplace_url: str = 'https://https://kwork.ru/'

    def __str__(self):
        text = (
            f'Появился новый заказ на {self.marketplace}!\n\n'
            '―――――――――――――――――――\n\n'
            f'Название: {self.title}\n\n'
            f'Заказчик: {md.hlink(self.customer_name, self.customer_url)}\n\n'
            f'Минимальная цена: {self.min_price}₽\n'
            f'💰 Цена: {self.price}\n'
            f'Максимальная цена: {self.max_price}₽\n\n'
            f'Описание: {self.description}\n\n'
            f'Количество откликов: {self.requests_count}\n\n'
            f'⏳ Дата: {self.date}\n'
            f'Дата завершения: {self.expire_date}\n\n'
            '―――――――――――――――――――'
        )

        return text


class InDevelopmentError(Exception):
    pass
