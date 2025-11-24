"""Modelo SQLAlchemy para usuarios.

Define la entidad `User` con campos de autenticación y relaciones con
workouts y plantillas creadas por el usuario.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    """Entidad que representa un usuario del sistema."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    """ Relaciones """
    workouts = relationship(
        "Workout", cascade="all, delete-orphan", back_populates="user"
    )
    templates = relationship(
        "WorkoutTemplate", cascade="all, delete-orphan", back_populates="creator"
    )
