from fastapi import APIRouter

router = APIRouter()


@router.post('/permissions')
async def create_permission():
    """Создает новый permission."""
    pass


@router.get('/permissions')
async def get_permissions():
    """Возвращает список всех permissions."""
    pass


@router.get('/permissions/{permission_id}')
async def get_permission():
    """Возвращает permission по id."""
    pass


@router.delete('/permissions/{permission_id}')
async def delete_permission():
    """Удаляет permission."""
    pass
