from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship

from config import DB_URL

engine = create_async_engine(url=DB_URL, echo=True)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)


class User(Base):
    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    channels = relationship("Channel", back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.user_name}, telegram_id: {self.telegram_id}"


class Channel(Base):
    id = Column(Integer, primary_key=True)
    channel_id = Column(String, nullable=False, unique=True)
    channel_name = Column(String, nullable=False, unique=True)
    last_video = Column(String, nullable=True, default="")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="channels")

    def __repr__(self):
        return f"Channel_id: {self.channel_name}, last video: {self.last_video}"
