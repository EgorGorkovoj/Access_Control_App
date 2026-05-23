from app.core.logging.logger import get_logger
from app.integrations.broker.interface import EventPublisher
from app.kafka.producer import KafkaProducerClient

logger = get_logger(__name__)


class KafkaEventPublisher(EventPublisher):
    def __init__(self, producer: KafkaProducerClient):
        self._producer = producer

    async def publish(self, topic: str, message: dict) -> None:
        try:
            await self._producer.send(topic=topic, value=message)

        except Exception:
            logger.exception(
                'Kafka publish failed',
                extra={
                    'topic': topic,
                    'message': message,
                },
            )
