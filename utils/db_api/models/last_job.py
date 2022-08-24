from ..base import Base

from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship


class LastJob(Base):
    __tablename__ = "last_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    weblancer_last_job = Column(String(255), nullable=True)
    habr_last_job = Column(String(255), nullable=True)
    freelance_last_job = Column(String(255), nullable=True)

    user = relationship("User", back_populates="last_jobs")