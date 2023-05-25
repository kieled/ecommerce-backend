from pydantic import BaseSettings


class RabbitConfig(BaseSettings):
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    @property
    def url(self):
        return "amqp://{}:{}@{}:{}/".format(
            self.RABBITMQ_DEFAULT_USER,
            self.RABBITMQ_DEFAULT_PASS,
            self.RABBITMQ_HOST,
            self.RABBITMQ_PORT
        )


rabbit_config = RabbitConfig()
