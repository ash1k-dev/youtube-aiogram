from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import Channel, User
from core.db.methods.request import get_user_from_db


async def create_user(user_name: str, telegram_id: int, session: AsyncSession) -> None:
    """Creating user"""
    user = User(user_name=user_name, telegram_id=telegram_id)
    session.add(user)
    await session.commit()


async def create_chanel(
    telegram_id: int,
    channel_id: str,
    channel_name: str,
    last_video: str,
    session: AsyncSession,
) -> None:
    """Creating channel"""
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    channel = Channel(
        channel_id=channel_id,
        channel_name=channel_name,
        last_video=last_video,
        user_id=user.id,
    )
    session.add(channel)
    await session.commit()
