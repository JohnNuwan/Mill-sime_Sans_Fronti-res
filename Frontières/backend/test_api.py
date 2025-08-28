"""
Test simple de l'API - Millésime Sans Frontières
Vérification que l'application démarre correctement
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Démarrage de l'API Millésime Sans Frontières...")
    print("📖 Documentation disponible sur: http://localhost:8000/docs")
    print("🔍 ReDoc disponible sur: http://localhost:8000/redoc")
    print("💚 Health check: http://localhost:8000/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
