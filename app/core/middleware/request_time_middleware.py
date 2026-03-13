import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


class RequestTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time_ms = round((time.time() - start_time) * 1000, 2)

        client_ip = request.headers.get("x-forwarded-for")
        if client_ip:
            client_ip = client_ip.split(",")[0]
        else:
            client_ip = request.client.host

        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time_ms": process_time_ms,
                "client_ip": client_ip
            }
        )

        response.headers["X-Process-Time"] = str(process_time_ms)

        return response