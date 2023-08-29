from core.db.database import engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=True)
    telegram_id = Column(Integer, nullable=False, unique=True)

    channels = relationship('User', back_populates='user')

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.user_name}, telegram_id: {self.telegram_id}"


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, nullable=True, unique=True)
    channel_name = Column(String, nullable=True, unique=True)
    last_video = Column(String, nullable=True, default='')
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='channels')

    def __repr__(self):
        return f"{self.__class__.__name__}, steam_id: {self.channel_name}"


# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)