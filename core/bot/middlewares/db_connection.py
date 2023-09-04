from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DbConnection(BaseMiddleware):
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
            data["session"] = session
            return await handler(event, data)
