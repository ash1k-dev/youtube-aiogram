from core.db.models.models import Channel, User

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


async def create_user(user_name: str, telegram_id: int, session: AsyncSession) -> None:
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
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    user = result.scalars().one_or_none()
    # user = User.query.filter(User.telegram_id == telegram_id)
    channel = Channel(
        channel_id=channel_id,
        channel_name=channel_name,
        last_video=last_video,
        user_id=user.id,
    )
    session.add(channel)
    await session.commit()
