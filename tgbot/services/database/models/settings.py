from sqlalchemy import Column, BigInteger, text, DateTime, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from tgbot.services.database.base import Base
from tgbot.services.database.models import User


class Settings(Base):
    __tablename__ = 'user_settings'

    user_id = Column(BigInteger, ForeignKey(User.telegram_id), primary_key=True, unique=True, autoincrement=False)
    include_filters = Column(Boolean, server_default=text('false'))
    subscribes = Column(MutableList.as_mutable(ARRAY(String(64))), default=[])

    user = relationship('User', lazy='selectin', back_populates='settings', uselist=False)
