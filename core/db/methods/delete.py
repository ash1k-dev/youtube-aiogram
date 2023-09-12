from sqlalchemy.ext.asyncio import AsyncSession

from core.db.methods.request import get_channel_from_db


async def delete_channel(channel_name: str, session: AsyncSession) -> None:
    channel = await get_channel_from_db(channel_name=channel_name, session=session)
    await session.delete(channel)
    await session.commit()
