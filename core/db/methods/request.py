from core.db.models.models import Channel, User

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


async def get_user_from_db(session: AsyncSession):
    statement = select(User)
    user = await session.execute(statement)
    return user.scalars().all()


async def get_channels_from_db(telegram_id: int, session: AsyncSession):
    statement = select(User).where(User.telegram_id == telegram_id)
    user = await session.execute(statement)
    user = user.scalars().one_or_none()
    channels = select(Channel).where(Channel.user_id == user.id)
    channels = await session.execute(channels)
    return channels.scalars().all()


# async def get_last_video_from_db(channel: Channel, session: AsyncSession):
#     statement = select(Channel).where(Channel.channel_id == channel)
#     channel = await session.execute(statement)
#     channel = channel.scalars().one_or_none()
#     return channel.last_video
