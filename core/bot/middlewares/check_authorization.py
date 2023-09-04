from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.db.methods.create import create_user
from core.db.models.models import User


class CheckAuthorization(BaseMiddleware):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession
        async with self.sessionmaker() as session:
            statement = select(User).where(User.telegram_id == event.from_user.id)
            result = await session.execute(statement)
            result = result.scalars().one_or_none()
            if result is None:
                await create_user(
                    user_name=event.from_user.full_name,
                    telegram_id=event.from_user.id,
                    session=session,
                )
        return await handler(event, data)
