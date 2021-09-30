from ..base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean


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
            return "Есть ✅"

        return "Нет ⛔️"

    async def get_habr(self):
        if self.habr_subscribe:
            return "Есть ✅"

        return "Нет ⛔️"

    async def sub_all(self):
        self.weblancer_subscribe = True
        self.habr_subscribe = True

        self.user.has_subscribes = True

    async def unsub_all(self):
        self.weblancer_subscribe = False
        self.habr_subscribe = False

        self.user.has_subscribes = False
