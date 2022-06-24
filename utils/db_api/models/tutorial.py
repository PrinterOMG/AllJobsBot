from ..base import Base

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Tutorial(Base):
    __tablename__ = "tutorial"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    show_filters = Column(Boolean, default=True)
    show_subscribes = Column(Boolean, default=True)

    user = relationship("User", back_populates="tutorial")

    async def reset_tutorial(self):
        self.show_subscribes = True
        self.show_filters = True
