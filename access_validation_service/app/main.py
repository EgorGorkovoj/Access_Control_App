import asyncio

from app.infrastructure.bootstrap.validation_application import ValidationApplication

# from app.infrastructure.http.management_client import AccessManagementClient
# from app.infrastructure.kafka.consumer import KafkaConsumerClient
from app.infrastructure.logging.logger import get_logger

# from app.infrastructure.config.settings import settings

logger = get_logger(f'{__name__}: kafka-test')


async def main():
    app = ValidationApplication()

    await app.run()


if __name__ == '__main__':
    asyncio.run(main())
