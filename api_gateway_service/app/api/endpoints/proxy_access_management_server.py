import httpx
from fastapi import APIRouter, Request, Response

access_router = APIRouter(prefix='/access_service')


@access_router.api_route(
    '/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
)
async def proxy_access(request: Request, path: str) -> Response:
    client: httpx.AsyncClient = request.app.state.http_registry.get('access_management')
    target_url = f'{client.base_url}/{path}'.rstrip('/')
    print(target_url)
    headers = dict(request.headers)
    headers.pop('host', None)
    headers.pop('content-length', None)

    try:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            content=await request.body(),
            follow_redirects=False,
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.RequestError as exc:
        return Response(content=f'Service unavailable: {exc}', status_code=503)
