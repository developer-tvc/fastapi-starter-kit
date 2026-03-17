import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import contextvars

correlation_id = contextvars.ContextVar("correlation_id", default=None)


class CorrelationIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

        correlation_id.set(cid)

        response = await call_next(request)

        response.headers["X-Correlation-ID"] = cid

        return response
