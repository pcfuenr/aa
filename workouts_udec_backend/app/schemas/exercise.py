"""Schemas Pydantic para ejercicios: entrada, actualización y representación en la API."""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.exercise import ExerciseType


class ExerciseBase(BaseModel):
    """Modelo base con campos comunes de un ejercicio."""
    name: str
    description: Optional[str] = None
    exercise_type: ExerciseType
    muscle_group: Optional[str] = None
    equipment: Optional[str] = None
    instructions: Optional[str] = None
    is_active: bool = True


class ExerciseCreate(ExerciseBase):
    """Schema para crear un nuevo ejercicio."""
    pass


class ExerciseUpdate(BaseModel):
    """Schema para actualizar parcialmente un ejercicio."""
    name: Optional[str] = None
    description: Optional[str] = None
    exercise_type: Optional[ExerciseType] = None
    muscle_group: Optional[str] = None
    equipment: Optional[str] = None
    instructions: Optional[str] = None
    is_active: Optional[bool] = None


class ExerciseInDBBase(ExerciseBase):
    """Campos adicionales presentes cuando el ejercicio está en la base de datos."""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Exercise(ExerciseInDBBase):
    """Schema expuesto por la API para un ejercicio persistido."""
    pass
