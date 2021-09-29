from ..base import Base

from sqlalchemy import Column, BigInteger, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    has_filters = Column(Boolean, default=False)
    has_subscribes = Column(Boolean, default=False)

    filters = relationship("Filter", uselist=False, back_populates="user")
    subscribes = relationship("Subscribe", uselist=False, back_populates="user")
    last_jobs = relationship("LastJob", uselist=False, back_populates="user")

    async def get_new_web_job(self, jobs):
        for job in jobs:
            if job.url == self.last_jobs.weblancer_last_job:
                return None

            if self.has_filters:
                if await self.filters.is_job_filtered(job):
                    self.last_jobs.weblancer_last_job = job.url
                    return job

                else:
                    self.last_jobs.weblancer_last_job = job.url
                    return None

            else:
                self.last_jobs.weblancer_last_job = job.url
                return job

    async def get_new_habr_job(self, job):
        if job.url == self.last_jobs.habr_last_job:
            return None

        if self.has_filters:
            if await self.filters.is_job_filtered(job):
                self.last_jobs.habr_last_job = job.url
                return job

            else:
                self.last_jobs.habr_last_job = job.url
                return None

        else:
            self.last_jobs.habr_last_job = job.url
            return job

    async def get_has_filters(self):
        if self.has_filters:
            return "Есть ✅"

        return "Нет ⛔️"

    async def get_has_subscribes(self):
        if self.has_subscribes:
            return "Есть ✅"

        return "Нет ⛔️"

    def __repr__(self):
        return f"Пользователь {self.id}"
