"""
FastAPI application entry point.
"""

# Standard library (none here)

# Third-party
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

# First-party (your app)
from app.core.config import settings
from app.core.security import limiter
from app.core.database import SessionLocal

# Routers
from app.modules.users.controllers.routes import router as users_router
from app.modules.auth.controllers.routes import router as auth_router
from app.modules.roles.controllers.routes import router as role_router
from app.modules.notifications.controllers.routes import router as notification_router
from app.modules.system.controllers.routes import router as system_router

# Middleware
from app.core.logging.middleware import CorrelationIdMiddleware
from app.core.logging.error_middleware import ErrorMiddleware
from app.core.middleware.request_time_middleware import RequestTimeMiddleware
from app.core.middleware.activity_context import activity_context_middleware
from app.core.middleware.cors_middleware import add_cors_middleware
from app.core.middleware.security_headers_middleware import SecurityHeadersMiddleware
from app.core.middleware.ip_whitelist_middleware import IPWhitelistMiddleware

# Services
from app.core.services.test_data_generator import seed_test_data


def create_app() -> FastAPI:
    """Create FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Startup Event for Test Data Generation
    @app.on_event("startup")
    def startup_event():
        """Initialize application on startup (seed test data in sandbox)."""
        if settings.ENVIRONMENT == "sandbox":
            db = SessionLocal()
            seed_test_data(db)
            db.close()

    # --------------------------------------------------
    # Rate Limiter Setup
    # --------------------------------------------------
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # --------------------------------------------------
    # Middleware Order (Important)
    # --------------------------------------------------

    # 1. Global Error Handler
    app.add_middleware(ErrorMiddleware)

    # 2. IP security
    app.add_middleware(IPWhitelistMiddleware)

    # 3. Correlation ID
    app.add_middleware(CorrelationIdMiddleware)

    # 4. Request Time Logging
    app.add_middleware(RequestTimeMiddleware)

    # 5. Security Headers
    app.add_middleware(SecurityHeadersMiddleware)

    # 6. Activity Logging Context
    app.middleware("http")(activity_context_middleware)

    # 7. CORS
    add_cors_middleware(app)

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

    app.include_router(
        notification_router,
        prefix="/api/v1/notifications",
        tags=["Notifications"],
    )

    app.include_router(
        system_router,
        prefix="/api/v1/system",
        tags=["System"],
    )

    return app


app = create_app()
