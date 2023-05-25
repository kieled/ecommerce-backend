from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from consumer.services import telegram_service
from shared.db import session_wrap, User, Settings
from shared.localizations import telegram as localizations


@session_wrap
async def mailing(message: str, session: AsyncSession):
    sql = select(User.telegram_chat_id).where(User.telegram_chat_id != None)
    telegram_ids = (await session.execute(sql)).scalars().all()
    await telegram_service.send_message(telegram_ids, message)


async def order_message(telegram_chat_id: str, order_id: int, message: str):
    message = localizations.order_message(order_id, message)
    await telegram_service.send_message(telegram_chat_id, message)


@session_wrap
async def admin_message(session: AsyncSession):
    sql = select(Settings).options(load_only(Settings.admin_chat_id))
    admin_chat_id = (await session.execute(sql)).scalars().first()
    await telegram_service.send_message(admin_chat_id, localizations.new_order_message)


__all__ = ['admin_message', 'mailing', 'order_message']
