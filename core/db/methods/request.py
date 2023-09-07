from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import Channel, User


async def get_user_from_db(message: Message, session: AsyncSession):
    statement = select(User).where(User.telegram_id == message.from_user.id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_users_from_db(session: AsyncSession):
    statement = select(User)
    user = await session.execute(statement)
    return user.scalars().all()


async def get_channel_from_db(
    channel_url: str, telegram_id: int, session: AsyncSession
):
    split_url = channel_url.split("/")
    for part in split_url:
        if part.startswith("@"):
            channel_id = part
    statement = select(User).where(User.telegram_id == telegram_id)
    user = await session.execute(statement)
    user = user.scalars().one_or_none()
    channel = select(Channel).where(
        Channel.user_id == user.id, Channel.channel_id == channel_id
    )
    channel = await session.execute(channel)
    return channel.scalars().one_or_none()


async def get_all_channels_from_db(telegram_id: int, session: AsyncSession):
    statement = select(User).where(User.telegram_id == telegram_id)
    user = await session.execute(statement)
    user = user.scalars().one_or_none()
    channels = select(Channel).where(Channel.user_id == user.id)
    channels = await session.execute(channels)
    return channels.scalars().all()
