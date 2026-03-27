# app/core/middleware/exceptions_middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import EmailAlreadyExists, PermissionDenied, UserNotFound


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Call the next middleware or route
            response = await call_next(request)
            return response
        except UserNotFound as e:
            return JSONResponse(status_code=404, content={"detail": str(e)})
        except EmailAlreadyExists as e:
            return JSONResponse(status_code=409, content={"detail": str(e)})
        except PermissionDenied as e:
            return JSONResponse(status_code=403, content={"detail": str(e)})
        except Exception as e:
            # Generic fallback for unexpected errors
            return JSONResponse(
                status_code=500, content={"detail": f"Internal Server Error: {str(e)}"}
            )

        # SQLAlchemy IntegrityError (duplicate email, etc.)
        except IntegrityError as e:
            # Optionally, you can check the exact constraint
            # For example: if "email" in str(e.orig)
            return JSONResponse(
                status_code=409,
                content={
                    "detail": "Database integrity error: likely duplicate or constraint violation"
                },
            )

        # Generic fallback for unexpected errors
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": f"Internal Server Error: {str(e)}"},
            )
