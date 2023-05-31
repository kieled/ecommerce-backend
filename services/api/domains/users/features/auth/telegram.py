import hashlib
import hmac
import time


def telegram_hash_check(bot_token: str, request_data: dict):
    request_data = request_data.copy()

    received_hash = request_data['hash']
    auth_date = request_data['auth_date']

    request_data.pop('hash', None)
    request_data_alphabetical_order = sorted(request_data.items(), key=lambda x: x[0])

    data_check_string = []

    for key, value in request_data_alphabetical_order:
        data_check_string.append(f'{key}={value}')

    data_check_string = '\n'.join(data_check_string)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    _hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)

    if unix_time_now - unix_time_auth_date > 86400:
        return False

    if _hash != received_hash:
        return False

    return True


__all__ = [
    'telegram_hash_check',
]
