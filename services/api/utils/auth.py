from passlib.context import CryptContext
import hashlib
import hmac

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def verify_telegram_auth(data, bot_token):
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
