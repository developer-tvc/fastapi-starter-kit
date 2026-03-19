from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.schemas.response import APIResponse  # your custom response wrapper

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"loc": e["loc"], "msg": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content=APIResponse.validation_error_response(
            message="Validation failed",
            errors=errors
        )
    )