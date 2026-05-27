import json
from typing import Any

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from app.core.config import settings
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


class KafkaProducerClient:
    def __init__(self) -> None:
        self.producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        if self.producer is not None:
            return

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda value: json.dumps(value).encode('utf-8'),
            acks='all',
            retry_backoff_ms=100,
            enable_idempotence=True,
            compression_type='gzip',
            linger_ms=10,
        )
        await self.producer.start()
        logger.info('Kafka Producer started')

    async def stop(self) -> None:
        if self.producer is None:
            return

        await self.producer.stop()
        self.producer = None
        logger.info('Kafka Producer stopped')

    async def send(self, topic: str, value: dict[str, Any], key: str | None = None) -> None:
        if self.producer is None:
            raise RuntimeError('Kafka producer not started')

        try:
            key_bytes = key.encode() if key else None

            await self.producer.send_and_wait(topic=topic, value=value, key=key_bytes)
            logger.debug(f'Sent to {topic}: {value}')
        except KafkaError as e:
            logger.error(f'Failed to send to {topic}: {e}')
            raise


producer_client = KafkaProducerClient()
