import random
import string
from datetime import datetime

from passlib.context import CryptContext
import hashlib
import hmac

from fastapi import Response

from strawberry.types import Info

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def verify_telegram_auth(data: dict, bot_token: str) -> bool:
    check_hash = data.pop('hash')
    check_list = ['{}={}'.format(k, v) for k, v in data.items()]
    check_string = '\n'.join(sorted(check_list))

    secret_key = hashlib.sha256(str.encode(bot_token)).digest()
    hmac_hash = hmac.new(
        secret_key,
        str.encode(check_string),
        hashlib.sha256,
    ).hexdigest()

    return hmac_hash == check_hash


def get_user_ids(info: Info) -> tuple[str | None, int | None]:
    temp_user_id = info.context.get('request').cookies.get('tempId')
    user_id = info.context.get('user_id')
    return temp_user_id, user_id


def add_random_temp_id_for_response(info: Info) -> str | None:
    temp_user_id, user_id = get_user_ids(info)
    if not temp_user_id and not user_id:
        temp_user_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        now = datetime.now()
        expires = int((datetime(
            day=now.day,
            month=now.month,
            year=now.year + 1
        )).timestamp())
        response: Response = info.context['response']
        response.set_cookie('tempId', temp_user_id, expires=expires)
        return temp_user_id
    return temp_user_id


__all__ = [
    'hash_password',
    'verify_password',
    'verify_telegram_auth',
    'get_user_ids',
    'add_random_temp_id_for_response'
]
