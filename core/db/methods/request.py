from core.db.models.models import Channel, User

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


async def get_channels_from_db(telegram_id: int, session: AsyncSession):
    statement = select(User).where(User.telegram_id == telegram_id)
    user = await session.execute(statement)
    user = user.scalars().one_or_none()
    channels = select(Channel).where(Channel.user_id == user.id)
    channels = await session.execute(channels)
    return channels.scalars().all()
