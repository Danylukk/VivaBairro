"""Fábrica da aplicação FastAPI e CORS estrito."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import Settings
from backend.app.routers.analises import router


def create_app(settings_override: Settings | None = None) -> FastAPI:
    settings = settings_override or Settings.from_env()
    settings.validate()
    app = FastAPI(title="VivaBairro — API CitizenTech", version="1.0.0", docs_url="/docs" if settings.app_env != "production" else None)
    app.state.settings = settings
    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
    app.include_router(router)
    return app


app = create_app()
