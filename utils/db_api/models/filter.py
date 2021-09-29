from ..base import Base
from data.config import TRANSLATE_TABLE

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship


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
                print(word)
                return True

        for word in self.description.split(";"):
            if word.lower() in job.description.lower().translate(TRANSLATE_TABLE).split():
                print(word)
                return True

        for tag in self.tags.split(";"):
            if tag.lower() in job.tags:
                print(tag)
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
