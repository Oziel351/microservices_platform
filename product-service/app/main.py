from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.excepcions import register_exception_handlers
from app.db.database import init_db, close_connection
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    init_db(str(settings.database_url))
    yield
    close_connection()

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Product service pro",
        version="1.0",
        docs_url="/docs" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(products_router)
    register_exception_handlers(app)

    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()