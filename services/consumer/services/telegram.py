import logging
from pyrogram import Client

from shared.base import telegram_config


class TelegramService:
    _client: Client

    def __init__(self):
        self._client = Client(
            'sender',
            telegram_config.TG_APP_ID,
            telegram_config.TG_APP_HASH,
            bot_token=telegram_config.TG_BOT_TOKEN,
            in_memory=True
        )

    async def send_message(self, ids: str | list[str], message_test: str) -> None:
        if not isinstance(ids, list):
            ids = [ids]
        async with self._client as client:
            for i in ids:
                try:
                    await client.send_message(int(i), message_test)
                except Exception as e:
                    logging.error(f'Failed to send telegram message to {i}\n{e}')


telegram_service = TelegramService()
