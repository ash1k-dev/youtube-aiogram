from core.db.database import session
from core.db.models.models import Channel, User


def create_user(user_name, telegram_id):
    user = User(
        user_name=user_name,
        telegram_id=telegram_id,
    )
    session.add(user)
    session.commit()


def create_chanel(telegram_id, channel_id, channel_name, last_video):
    user = User.query.filter(User.telegram_id == telegram_id)
    channel = Channel(
        channel_id=channel_id,
        channel_name=channel_name,
        last_video=last_video,
        user_id=user.id,
    )
    session.add(channel)
    session.commit()
