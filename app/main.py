from fastapi import FastAPI
from app.core.config import settings
from app.modules.users.controllers.routes import router as users_router

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

    return app


app = create_app()
