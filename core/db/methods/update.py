from core.db.models.models import Channel, User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def update_last_video(
    channel: str, last_video: str, session: AsyncSession
) -> None:
    statement = select(Channel).where(Channel.channel_id == channel)
    result = await session.execute(statement)
    channel = result.scalars().one_or_none()
    channel.last_video = last_video
    session.add(channel)
    await session.commit()
