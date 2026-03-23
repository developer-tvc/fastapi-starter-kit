from fastapi import Request

from app.modules.activity_logs.request_context import current_ip


async def activity_context_middleware(request: Request, call_next):

    if request.client:
        current_ip.set(request.client.host)

    response = await call_next(request)

    return response
