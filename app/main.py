from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.routes import router

def create_app() -> FastAPI:
    app = FastAPI(title="Document AI Backend (Backend-only)")
    Base.metadata.create_all(bind=engine)  # Phase 1 simple auto-create tables
    app.include_router(router)
    return app

app = create_app()
