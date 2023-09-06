from core.db.models.models import Channel, User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# async def delete_user(telegram_id: int, session: AsyncSession) -> None:
#     statement = select(User).where(User.telegram_id == telegram_id)
#     result = await session.execute(statement)
#     await session.delete(result)
#     await session.commit()
#


async def delete_channel(channel_id: str, session: AsyncSession) -> None:
    statement = select(Channel).where(Channel.channel_id == channel_id)
    channel = await session.execute(statement)
    channel = channel.scalars().one_or_none()
    await session.delete(channel)
    await session.commit()
