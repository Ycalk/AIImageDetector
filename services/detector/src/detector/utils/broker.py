from faststream.rabbit import RabbitBroker
from .config import Config


broker = RabbitBroker(
    f"amqp://{Config.RABBIT_USER}:{Config.RABBIT_PASSWORD}@{Config.RABBIT_HOST}:{Config.RABBIT_PORT}/"
)
