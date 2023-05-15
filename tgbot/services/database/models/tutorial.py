from sqlalchemy import Column, BigInteger, text, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from tgbot.services.database.base import Base
from tgbot.services.database.models import User


class Tutorial(Base):
    __tablename__ = 'user_tutorial'

    user_id = Column(BigInteger, ForeignKey(User.telegram_id), primary_key=True, unique=True, autoincrement=False)
    show_filters = Column(Boolean, server_default=text('true'))
    show_subscribes = Column(Boolean, server_default=text('true'))

    user = relationship('User', lazy='selectin', back_populates='tutorial', uselist=False)

    def reset_tutorial(self):
        self.show_filters = True
        self.show_subscribes = True
