"""Configuración del motor y fábrica de sesiones de SQLAlchemy.

Este módulo expone `engine` y `SessionLocal` para obtener sesiones de DB.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
"""Fábrica de sesiones: llamar a SessionLocal() para obtener una nueva sesión."""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
