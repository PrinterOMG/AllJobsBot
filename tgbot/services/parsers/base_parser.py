from abc import ABC, abstractmethod

from tgbot.services.parsers.schemas import Job


class Parser(ABC):
    @property
    @abstractmethod
    def marketplace_name(self):
        pass

    @property
    @abstractmethod
    def marketplace_url(self):
        pass

    @property
    @abstractmethod
    def jobs_list_url(self):
        pass

    @classmethod
    @abstractmethod
    async def parse_last_job(cls) -> Job | None:
        pass

    @classmethod
    @abstractmethod
    async def parse_job_with_url(cls, url: str) -> Job | None:
        pass

