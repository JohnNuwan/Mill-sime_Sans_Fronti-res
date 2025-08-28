"""
Configuration de la base de données - Millésime Sans Frontières
Gestion de la connexion SQLAlchemy et sessions
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_database_url, settings

# Création de l'engine SQLAlchemy
if settings.DEBUG:
    # Mode développement avec SQLite en mémoire
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
else:
    # Mode production avec PostgreSQL
    engine = create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )

# Création de la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialisation de la base de données"""
    # Import des modèles pour qu'ils soient connus de SQLAlchemy
    from app.models import user, barrel, order, quote, address
    
    # Création des tables
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès!")


def close_db():
    """Fermeture de la connexion à la base de données"""
    engine.dispose()
    print("Connexion à la base de données fermée.")


def create_tables():
    """Crée toutes les tables de la base de données"""
    # Import des modèles pour qu'ils soient connus de SQLAlchemy
    from app.models import user, barrel, order, quote, address
    
    # Création des tables
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès!")


def drop_tables():
    """Supprime toutes les tables de la base de données"""
    # Suppression des tables
    Base.metadata.drop_all(bind=engine)
    print("Tables supprimées avec succès!")
