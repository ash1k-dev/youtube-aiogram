from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    DeclarativeBase,
    declared_attr,
)

import asyncio

from config import DB_URL

engine = create_async_engine(url=DB_URL, echo=True)

# Base = declarative_base()


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
    channel_id = Column(String, nullable=True, unique=True)
    channel_name = Column(String, nullable=True, unique=True)
    last_video = Column(String, nullable=True, default="")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="channels")

    def __repr__(self):
        return f"Channel_id: {self.channel_name}, last video: {self.last_video}"


# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# connection = psycopg2.connect(user="postgres", password="postgres")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#
# cursor = connection.cursor()
# sql_create_database = (
#     DB_URL
# ) = "postgresql+asyncpg://postgres:postgres@localhost/youtube"
# cursor.execute("create database youtube")
# cursor.close()
# connection.close()


# async def init_models():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#
# asyncio.run(init_models())
