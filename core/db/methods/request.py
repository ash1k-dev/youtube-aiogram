from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import Channel, User


async def get_user_from_db(telegram_id: int, session: AsyncSession):
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_channel_from_db(channel_name: str, session: AsyncSession):
    statement = select(Channel).where(Channel.channel_name == channel_name)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_users_from_db(session: AsyncSession):
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()


async def check_channel_in_db(
    channel_url: str, telegram_id: int, session: AsyncSession
):
    split_url = channel_url.split("/")
    for part in split_url:
        if part.startswith("@"):
            channel_id = part
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = select(Channel).where(
        Channel.user_id == user.id, Channel.channel_id == channel_id
    )
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_channels_from_db(telegram_id: int, session: AsyncSession):
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = select(Channel).where(Channel.user_id == user.id)
    result = await session.execute(statement)
    return result.scalars().all()
