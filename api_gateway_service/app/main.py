import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response, status

# access_service это часть пути по которому будет проводиться переадресация!
SERVICES = {
    'access_service': os.getenv('ACCESS_MANAGEMENT_SERVICE_URL', 'http://localhost:8001'),
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()
    try:
        yield
    finally:
        await app.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)

# Получаем URL сервисов из переменных окружения
ACCESS_MANAGEMENT_SERVICE_URL = os.getenv('ACCESS_MANAGEMENT_SERVICE_URL')


@app.api_route('/{full_path:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
async def proxy_request(request: Request, full_path: str) -> Response:
    """
    Эта функция определяет, какому сервису перенаправить запрос,
    основываясь на начальной части URL-пути.
    """
    parts = full_path.split('/', 1)
    service_key = parts[0]
    path_after_service = '/' + parts[1] if len(parts) > 1 else '/'

    target_base = SERVICES.get(service_key)
    if not target_base:
        return Response(content='Service Not Found', status_code=status.HTTP_404_NOT_FOUND)
    target_url = f'{target_base}{path_after_service}'
    # target_url = None
    # if path.startswith('access_management_service'):
    #     target_url = f'{ACCESS_MANAGEMENT_SERVICE_URL}/{path}'

    # if not target_url:
    #     return Response(content='Not Found', status_code=status.HTTP_404_NOT_FOUND)

    # Получаем тело запроса
    body = await request.body()

    # Формируем запрос к целевому сервису
    proxied_req = app.state.http_client.build_request(
        method=request.method,
        url=target_url,
        headers=request.headers,
        params=request.query_params,
        content=body,
    )

    # Отправляем запрос
    response = await app.state.http_client.send(proxied_req)

    # Возвращаем ответ клиенту
    return Response(
        content=response.content, status_code=response.status_code, headers=dict(response.headers)
    )
