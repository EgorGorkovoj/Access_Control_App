from fastapi import APIRouter

router = APIRouter()


@router.post('/groups/{group_id}/accesses/{permission_id}')
async def add_access_to_group():
    """Назначает access группе."""
    pass


@router.delete('/groups/{group_id}/accesses/{permission_id}')
async def remove_permission_from_group():
    """Удаляет access у группы."""
    pass


@router.get('/groups/{group_id}/accesses')
async def get_group_accesses():
    """Возвращает список accesses группы."""
    pass
