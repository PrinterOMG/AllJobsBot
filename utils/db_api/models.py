from sqlalchemy import create_engine, MetaData, Table, Integer, Text, Column, ForeignKey, Numeric, BigInteger, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from data.config import DATABASE_URL, TRANSLATE_TABLE

Base = declarative_base()
engine = create_engine(DATABASE_URL)


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
                if self.filters.is_job_filtered(job):
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
            if self.filters.is_job_filtered(job):
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
            return "Есть"

        return "Нет"

    async def get_has_subscribes(self):
        if self.has_subscribes:
            return "Есть"

        return "Нет"

    def __repr__(self):
        return f"Пользователь {self.id}"


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    title = Column(Text, nullable=True, default="")
    description = Column(Text, nullable=True, default="")
    tags = Column(Text, nullable=True, default="")
    category = Column(Text, nullable=True, default="")

    user = relationship("User", back_populates="filters")

    async def is_job_filtered(self, job):
        for word in self.title.split(";"):
            if word.lower() in job.title.lower().translate(TRANSLATE_TABLE).split():
                return True

        for word in self.description.split(";"):
            if word.lower() in job.description.lower().translate(TRANSLATE_TABLE).split():
                return True

        for tag in self.tags.split(";"):
            if tag.lower() in job.tags:
                return True

        return False

    async def clear_all(self):
        self.tags = ""
        self.description = ""
        self.category = ""
        self.title = ""

        self.user.has_filters = False

    async def check(self):
        if self.tags or self.title or self.description or self.category:
            self.user.has_filters = True
        else:
            self.user.has_filters = False

    async def get_title(self):
        title = self.title.split(";")

        return ", ".join(title)

    async def get_description(self):
        description = self.description.split(";")

        return ", ".join(description)

    async def get_tags(self):
        tags = self.tags.split(";")

        return ", ".join(tags)


class Subscribe(Base):
    __tablename__ = "subscribes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    weblancer_subscribe = Column(Boolean, default=False)
    habr_subscribe = Column(Boolean, default=False)

    user = relationship("User", back_populates="subscribes")

    async def check(self):
        if self.weblancer_subscribe or self.habr_subscribe:
            self.user.has_subscribes = True
        else:
            self.user.has_subscribes = False

    async def get_weblancer(self):
        if self.weblancer_subscribe:
            return "Есть"

        return "Нет"

    async def get_habr(self):
        if self.habr_subscribe:
            return "Есть"

        return "Нет"


class LastJob(Base):
    __tablename__ = "last_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    weblancer_last_job = Column(String(200), nullable=True)
    habr_last_job = Column(String(200), nullable=True)

    user = relationship("User", back_populates="last_jobs")


Base.metadata.create_all(engine)
