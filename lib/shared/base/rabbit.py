from pydantic import BaseSettings


class RabbitConfig(BaseSettings):
    RABBITMQ_DEFAULT_USER: str = 'admin'
    RABBITMQ_DEFAULT_PASS: str = 'admin'
    RABBITMQ_HOST: str = 'rabbit'
    RABBITMQ_PORT: int = 5672

    @property
    def url(self):
        return "amqp://{}:{}@{}:{}/".format(
            self.RABBITMQ_DEFAULT_USER,
            self.RABBITMQ_DEFAULT_PASS,
            self.RABBITMQ_HOST,
            self.RABBITMQ_PORT
        )


rabbit_config = RabbitConfig()
