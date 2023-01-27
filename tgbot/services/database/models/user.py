from sqlalchemy import Column, BigInteger, text, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from tgbot.services.database.base import Base


class User(Base):
    __tablename__ = 'telegram_user'

    telegram_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    name = Column(String(128))
    username = Column(String(128), nullable=True)
    email = Column(String(128), nullable=True, unique=True)
    phone = Column(String(20), nullable=True, unique=True)
    is_reg = Column(Boolean, server_default=text('false'))
    created_at = Column(DateTime(), server_default=text('NOW()'))
    referral_id = Column(BigInteger, ForeignKey(telegram_id))

    courier = relationship('Courier', lazy='selectin', uselist=False)
    operator = relationship('Operator', lazy='selectin', back_populates='user', uselist=False)
    referral = relationship('Referral', lazy='selectin', foreign_keys='[Referral.telegram_id]', uselist=False)
