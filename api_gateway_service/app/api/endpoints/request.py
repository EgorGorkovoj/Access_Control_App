from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.logging.logger import get_logger
from app.dependencies.http import get_http_factory
from app.dependencies.kafka import get_event_publisher
from app.integrations.broker.interface import EventPublisher
from app.integrations.http.factory import HttpClientFactory
from app.shemas.request import AccessRequestResponseSchema, CreateAccessRequestSchema

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    '/access-requests/right-groups',
    response_model=AccessRequestResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_access_request(
    body: CreateAccessRequestSchema,
    factory: HttpClientFactory = Depends(get_http_factory),
    publisher: EventPublisher = Depends(get_event_publisher),
) -> AccessRequestResponseSchema:
    request_id = str(uuid4())
    client = factory.access_management()

    event = {
        'request_id': request_id,
        'user_id': body.user_id,
        'target_type': body.target_type,
        'target_id': body.target_id,
    }
    try:
        await client.post('/api/v1/request', json=event)
    except Exception as error:
        logger.error(
            f'Failed to call access_management service:{error}',
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail='Access management service unavailable',
        )

    await publisher.publish(
        topic=settings.ACCESSES_TOPIC,
        message=event,
    )

    return AccessRequestResponseSchema(
        request_id=request_id,
    )
