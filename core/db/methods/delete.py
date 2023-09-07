from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import Channel, User


async def delete_channel(channel_name: str, session: AsyncSession) -> None:
    statement = select(Channel).where(Channel.channel_name == channel_name)
    channel = await session.execute(statement)
    channel = channel.scalars().one_or_none()
    await session.delete(channel)
    await session.commit()
