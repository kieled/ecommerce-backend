import json

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustExchange, ExchangeType

from shared.base import rabbit_config
from shared.schemas import MessageSchema


class RabbitConnection:
    _connection: AbstractRobustConnection | None = None
    _channel: AbstractRobustChannel | None = None
    _exchange: AbstractRobustExchange | None = None

    async def disconnect(self) -> None:
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None

    async def connect(self) -> None:
        try:
            self._connection = await connect_robust(rabbit_config.url)
            self._channel = await self._connection.channel(publisher_confirms=False)
            self._exchange = await self._channel.declare_exchange(
                'main', ExchangeType.X_DELAYED_MESSAGE,
                arguments={
                    'x-delayed-type': 'direct'
                }
            )
        except Exception as e:
            await self.disconnect()

    async def send_messages(
            self,
            messages: list[MessageSchema],
            *,
            routing_key: str = rabbit_config.RABBITMQ_QUEUE,
            delay: int = None
    ) -> None:
        async with self._channel.transaction():
            headers = None
            if delay:
                headers = {
                    'x-delay': f'{delay * 1000}'
                }
            for message in messages:
                message = Message(
                    body=json.dumps(message.dict()).encode(),
                    headers=headers
                )
                await self._exchange.publish(
                    message,
                    routing_key=routing_key,
                    mandatory=False if delay else True
                )


rabbit_connection = RabbitConnection()
