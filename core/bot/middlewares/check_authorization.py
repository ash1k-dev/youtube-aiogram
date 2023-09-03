from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.orm import Session
from core.db.database import session
from core.db.models.models import User
from core.db.methods.create import create_user


class CheckAuthorization(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user = (
            session.query(User).filter(User.telegram_id == event.from_user.id).first()
        )
        if user:
            pass
        else:
            create_user(
                user_name=event.from_user.first_name, telegram_id=event.from_user.id
            )
        return await handler(event, data)
