import asyncio
import inspect
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from shared.base import rabbit_config
from shared.schemas import MessageSchema

from consumer.router import router


async def process_message(message: AbstractIncomingMessage):
    async with message.process():
        message = MessageSchema.parse_obj(json.loads(message.body.decode()))
        method = router.get_method(message.action)
        if method:
            if not router.check_args(method, message.body):
                print('Invalid args')
                return
            if inspect.iscoroutinefunction(method):
                await method(**message.body)
            else:
                method(**message.body)


async def main() -> None:
    queue_key = rabbit_config.RABBITMQ_QUEUE

    connection = await aio_pika.connect_robust(rabbit_config.url)
    channel = await connection.channel(publisher_confirms=False)
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(queue_key)

    exchange = await channel.declare_exchange(
        'main', ExchangeType.X_DELAYED_MESSAGE,
        arguments={
            'x-delayed-type': 'direct'
        }
    )
    await queue.bind(exchange, queue_key)
    await queue.consume(process_message)
    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
