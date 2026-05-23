from app.kafka.producer import producer_client
from app.kafka.publisher import KafkaEventPublisher

publisher = KafkaEventPublisher(producer_client)


def get_event_publisher() -> KafkaEventPublisher:
    return publisher
