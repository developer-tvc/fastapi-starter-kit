from fastapi import FastAPI, Request

from app.core.config import settings

from app.modules.users.controllers.routes import router as users_router
from app.modules.auth.controllers.routes import router as auth_router
from app.modules.roles.controllers.routes import router as role_router

from app.modules.activity_logs.request_context import current_ip


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # -----------------------------
    # Activity Log Middleware
    # -----------------------------
    @app.middleware("http")
    async def activity_context_middleware(request: Request, call_next):

        # Capture client IP
        if request.client:
            current_ip.set(request.client.host)

        response = await call_next(request)

        return response

    # -----------------------------
    # Routers
    # -----------------------------

    app.include_router(
        users_router,
        prefix="/api/v1/users",
        tags=["Users"],
    )

    app.include_router(
        auth_router,
        prefix="/api/v1/auth",
        tags=["Auth"],
    )

    app.include_router(
        role_router,
        prefix="/api/v1/role",
        tags=["Permissions Management"],
    )

    return app


app = create_app()