from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.routes import router

def create_app() -> FastAPI:
    # Create and configure the FastAPI application instance
    app = FastAPI(title="Document AI Backend (Backend-only)")
    
    # Create all database tables defined in SQLAlchemy models
    # This binds the metadata to the engine and ensures tables exist at startup
    Base.metadata.create_all(bind=engine)
    
    # Register all API routes with the FastAPI application
    app.include_router(router)
    
    # Return the fully configured application instance
    return app

# Initialize the FastAPI application for ASGI servers 
app = create_app()
