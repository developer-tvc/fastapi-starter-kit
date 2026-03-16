from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.config import settings


class IPWhitelistMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host

        if settings.IP_WHITELIST_ENABLED:

            if client_ip not in settings.ALLOWED_IPS:
                return JSONResponse(
                    status_code=403, content={"detail": "IP not allowed"}
                )

        return await call_next(request)
