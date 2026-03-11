from fastapi import FastAPI
from app.core.config import settings
from app.modules.users.controllers.routes import router as users_router
from app.modules.auth.controllers.routes import router as auth_router
from app.modules.roles.controllers.routes import router as role_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.include_router(
        users_router,
        prefix="/api/v1/users",
        tags=["Users"],
    )  # User module router
    app.include_router(
        auth_router,
        prefix="/api/v1/auth",
        tags=["Auth"],
    )  # Auth module router

    app.include_router(
        role_router,
        prefix="/api/v1/role",
        tags=["Permissions Management"],
    )

    return app


app = create_app()
