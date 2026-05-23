from app.integrations.broker.interface import EventPublisher


class UserService:
    def __init__(self, publisher: EventPublisher):
        self.publisher = publisher

    # TODO: поменять логику плюс возможно добавить в параметр топик!
    async def create_user(self, user_id: str):
        # бизнес-логика
        print(f'Creating user {user_id}')

        await self.publisher.publish('user_created', user_id.encode())
