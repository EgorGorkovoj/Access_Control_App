from fastapi import APIRouter

router = APIRouter()


@router.post('/groups/{group_id}/conflicts/{conflicting_group_id}')
async def add_group_conflict():
    """Добавляет конфликт между двумя группами."""
    pass


@router.delete('/groups/{group_id}/conflicts/{conflicting_group_id}')
async def remove_group_conflict():
    """Удаляет конфликт групп."""
    pass


@router.get('/groups/{group_id}/conflicts')
async def get_group_conflicts():
    """Возвращает список конфликтующих групп."""
    pass
