from ..base import Base
from data.config import TRANSLATE_TABLE

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    key_words = Column(Text, nullable=True, default="")

    user = relationship("User", back_populates="filters")

    async def is_job_filtered(self, job):
        for word in self.key_words.split(";"):
            if word.lower() in job.title.lower().translate(TRANSLATE_TABLE).split():
                return True

        return False

    async def check(self):
        if self.key_words:
            self.user.has_filters = True
        else:
            self.user.has_filters = False

    async def get_keywords(self):
        if self.key_words:
            key_words = self.key_words.split(";")

            return ", ".join(key_words)
        else:
            return "Не заданы"
