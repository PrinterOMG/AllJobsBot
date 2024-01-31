import string

from sqlalchemy import Column, BigInteger, text, DateTime, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from tgbot.services.database.base import Base
from tgbot.services.database.models import User
from tgbot.services.parsers.schemas import Job


class Filter(Base):
    __tablename__ = 'user_filter'

    user_id = Column(BigInteger, ForeignKey(User.telegram_id), primary_key=True, unique=True, autoincrement=False)
    filter_words = Column(ARRAY(String(64)), default=[])

    user = relationship('User', lazy='selectin', back_populates='filters', uselist=False)

    def filter_job(self, job: Job) -> bool:
        text_for_search = job.title + ' ' + job.description

        translate_table = str.maketrans(dict.fromkeys(string.punctuation))
        for word in self.filter_words:
            if word.lower() in text_for_search.lower().translate(translate_table).split():
                return True

        return False
