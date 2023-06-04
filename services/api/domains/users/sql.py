from sqlalchemy import update, insert, select
from sqlalchemy.orm import load_only

from shared.db import User


def update_first_name(first_name: str, chat_id: str):
    return update(User).where(User.telegram_chat_id == chat_id).values(
        first_name=first_name
    )


def add_new(payload: dict):
    return insert(User).values(**payload).returning(User.telegram_chat_id)


def user_type(user_id: int):
    return select(User).options(load_only(User.id, User.type)).where(User.id == user_id)


def user_by_telegram(telegram_chat_id: str):
    return select(User).options(load_only(User.id, User.type)).where(User.telegram_chat_id == telegram_chat_id)


def user_by_username(username: str):
    return select(User).options(load_only(User.id)).where(User.username == username)
