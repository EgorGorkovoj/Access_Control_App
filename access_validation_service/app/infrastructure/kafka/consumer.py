import asyncio
import json
from typing import Awaitable, Callable

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError, KafkaError
from app.infrastructure.config.settings import settings
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class KafkaConsumerClient:
    def __init__(
        self,
        topic: str,
        handler: Callable[[dict], Awaitable[None]],
        group_id: str | None = None,
    ):
        self.topic = topic
        self.handler = handler
        self.group_id = group_id or settings.KAFKA_CONSUMER_GROUP
        self.consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.group_id,
            auto_offset_reset=settings.KAFKA_AUTO_OFFSET_RESET,
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )

        retries = 10

        for attempt in range(retries):
            try:
                await self.consumer.start()
                logger.info('Consumer started: topic=%s', self.topic)
                break
            except KafkaConnectionError:
                logger.warning('Kafka not ready (%s/%s)', attempt + 1, retries)
                await asyncio.sleep(3)

        else:
            raise KafkaConnectionError(f'Failed to connect to Kafka after {retries} attempts')
        self._task = asyncio.create_task(self._consume_loop())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        if self.consumer:
            await self.consumer.stop()
        logger.info('Consumer stopped: topic=%s', self.topic)

    async def _consume_loop(self) -> None:
        if self.consumer is None:
            raise RuntimeError('Consumer not initialized')

        try:
            async for message in self.consumer:
                try:
                    await self.handler(message.value)
                    await self.consumer.commit()

                    logger.info(
                        'Message processed: topic=%s offset=%s', message.topic, message.offset
                    )

                except Exception:
                    logger.exception(
                        'Message processing failed: ' 'topic=%s partition=%s offset=%s',
                        message.topic,
                        message.partition,
                        message.offset,
                    )

        except asyncio.CancelledError:
            logger.info('Consumer loop cancelled: topic=%s', self.topic)
            raise
        except KafkaError:
            logger.exception('Kafka consumer error: topic=%s', self.topic)
        except Exception:
            logger.exception('Unexpected consumer error: topic=%s', self.topic)
