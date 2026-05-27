import asyncio

from app.infrastructure.bootstrap.validation_application import ValidationApplication
from app.infrastructure.logging.config import setup_logging

setup_logging()


async def main():
    app = ValidationApplication()
    await app.run()


if __name__ == '__main__':
    asyncio.run(main())
