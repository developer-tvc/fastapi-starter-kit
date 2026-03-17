"""
ErrorMiddleware is a middleware that catches all exceptions and returns a JSON response.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


class ErrorMiddleware(BaseHTTPMiddleware):
    """
    ErrorMiddleware is a middleware that catches all exceptions and returns a JSON response.
    """
    async def dispatch(self, request, call_next):
        """
        Dispatches the request to the next middleware.
        """
        try:
            return await call_next(request)

        except HTTPException as exc:
            # Allow FastAPI HTTP errors to pass through
            return JSONResponse(
                status_code=exc.status_code, content={"detail": exc.detail}
            )

        except Exception as e:

            logger.error(f"Unhandled error: {str(e)}")

            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )
