from sqlalchemy.ext.asyncio import AsyncSession

from core.db.methods.request import get_channel_from_db


async def update_last_video(
    channel_name: str, last_video: str, session: AsyncSession
) -> None:
    """Latest video update"""
    channel = await get_channel_from_db(channel_name=channel_name, session=session)
    channel.last_video = last_video
    session.add(channel)
    await session.commit()
