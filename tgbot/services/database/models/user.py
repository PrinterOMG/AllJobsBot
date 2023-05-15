from sqlalchemy import Column, BigInteger, text, DateTime, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import array, ARRAY
from sqlalchemy.orm import relationship

from tgbot.services.database.base import Base
from tgbot.services.parsers.schemas import Job
from tgbot.services.utils import pretty_bool


class User(Base):
    __tablename__ = 'telegram_user'

    telegram_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    created_at = Column(DateTime(), server_default=text('NOW()'))

    filters = relationship('Filter', lazy='selectin', back_populates='user', uselist=False)
    settings = relationship('Settings', lazy='selectin', back_populates='user', uselist=False)
    tutorial = relationship('Tutorial', lazy='selectin', back_populates='user', uselist=False)

    @property
    def has_filters(self):
        return pretty_bool(self.settings.include_filters)

    @property
    def has_subscribes(self):
        return pretty_bool(self.settings.subscribes)
