"""
Application principale FastAPI - Millésime Sans Frontières
Backend pour le site e-commerce de fûts de vin
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Créer les tables au démarrage
    Base.metadata.create_all(bind=engine)
    yield


# Création de l'application FastAPI
app = FastAPI(
    title="Millésime Sans Frontières API",
    description="API backend pour le site e-commerce de fûts de vin",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes API
app.include_router(api_router, prefix="/v1")


@app.get("/")
async def root():
    """Route racine de l'API"""
    return JSONResponse(
        content={
            "message": "Bienvenue sur l'API Millésime Sans Frontières",
            "version": "1.0.0",
            "status": "running"
        },
        status_code=200
    )


@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {"status": "healthy", "service": "Millésime Sans Frontières API"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
