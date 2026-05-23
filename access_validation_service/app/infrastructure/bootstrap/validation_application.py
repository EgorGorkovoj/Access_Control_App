from app.infrastructure.config.settings import settings
from app.infrastructure.dependencies import (
    get_validation_service,
)
from app.infrastructure.http.management_client import AccessManagementClient
from app.infrastructure.kafka.consumer import KafkaConsumerClient
from app.infrastructure.kafka.handlers.access_request_handler import AccessRequestHandler
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ValidationApplication:
    def __init__(self) -> None:
        self.client: AccessManagementClient | None = None
        self.consumer: KafkaConsumerClient | None = None

    async def start(self) -> None:
        logger.info('Starting Validation Service...')

        self.client = AccessManagementClient(
            base_url=settings.ACCESS_MANAGEMENT_SERVICE_URL,
        )

        await self.client.start()

        validation_service = get_validation_service(self.client)

        handler = AccessRequestHandler(validation_service)

        self.consumer = KafkaConsumerClient(
            topic=settings.ACCESSES_TOPIC,
            handler=handler.handle,
            group_id=settings.KAFKA_CONSUMER_GROUP,
        )

        await self.consumer.start()

        logger.info('Validation Service started')

    async def stop(self) -> None:
        if self.consumer:
            await self.consumer.stop()

        if self.client:
            await self.client.stop()

        logger.info('Validation Service stopped')

    async def run(self) -> None:
        await self.start()

        if self.consumer is None:
            raise RuntimeError('Consumer not initialized')

        try:
            logger.info('Validation Service started')

            await self.consumer.run()

        finally:
            await self.stop()
