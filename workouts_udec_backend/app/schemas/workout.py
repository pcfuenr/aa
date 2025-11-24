"""Schemas Pydantic para plantillas de entrenamiento, ejercicios y sets.

Contiene los modelos usados por la API para crear, actualizar y listar workouts
y plantillas.
"""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.exercise import Exercise


class WorkoutTemplateExerciseBase(BaseModel):
    """Modelo base para ejercicios dentro de una plantilla (sugerencias)."""
    exercise_id: int
    order_index: int
    suggested_sets: Optional[int] = None
    suggested_reps: Optional[int] = None
    suggested_weight: Optional[float] = None
    suggested_duration: Optional[int] = None


class WorkoutTemplateExerciseCreate(WorkoutTemplateExerciseBase):
    """Schema para añadir un ejercicio a una plantilla."""
    pass


class WorkoutTemplateExercise(WorkoutTemplateExerciseBase):
    """Representación completa de un ejercicio dentro de una plantilla."""
    id: int
    template_id: int
    exercise: Exercise

    class Config:
        from_attributes = True


class WorkoutTemplateBase(BaseModel):
    """Campos básicos de una plantilla de entrenamiento."""
    name: str
    description: Optional[str] = None
    is_public: bool = False


class WorkoutTemplateCreate(WorkoutTemplateBase):
    """Schema para crear una plantilla incluyendo sus ejercicios."""
    exercises: List[WorkoutTemplateExerciseCreate] = []


class WorkoutTemplateUpdate(BaseModel):
    """Schema para actualizar una plantilla de entrenamiento."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class WorkoutTemplate(WorkoutTemplateBase):
    """Plantilla completa con metadatos y ejercicios asociados."""
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    template_exercises: List[WorkoutTemplateExercise] = []

    class Config:
        from_attributes = True


class ExerciseSetBase(BaseModel):
    """Modelo base para un set dentro de un ejercicio."""
    set_number: int
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration: Optional[int] = None
    rest_duration: Optional[int] = None
    completed: bool = False


class ExerciseSetCreate(ExerciseSetBase):
    """Schema para crear un set en un ejercicio durante el workout."""
    pass


class ExerciseSetUpdate(BaseModel):
    """Schema para actualizar un set existente."""
    set_number: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration: Optional[int] = None
    rest_duration: Optional[int] = None
    completed: Optional[bool] = None


class ExerciseSet(ExerciseSetBase):
    """Representación de un set ya persistido (con id)."""
    id: int

    class Config:
        from_attributes = True


class WorkoutExerciseBase(BaseModel):
    """Campos básicos para un ejercicio dentro de un workout."""
    exercise_id: int
    order_index: int
    notes: Optional[str] = None


class WorkoutExerciseCreate(WorkoutExerciseBase):
    """Schema para crear un ejercicio dentro de un workout (incluye sets)."""
    sets: List[ExerciseSetCreate] = []


# Need to import Exercise schema to avoid circular imports
from app.schemas.exercise import Exercise


class WorkoutExercise(WorkoutExerciseBase):
    """Ejercicio asociado a un workout con sus sets y metadatos."""
    id: int
    workout_id: int
    exercise: Exercise
    sets: List[ExerciseSet] = []

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    """Campos básicos de un workout (sesión de entrenamiento)."""
    name: Optional[str] = None
    notes: Optional[str] = None
    template_id: Optional[int] = None


class WorkoutCreate(WorkoutBase):
    """Schema para crear un workout completo con ejercicios."""
    exercises: List[WorkoutExerciseCreate] = []


class WorkoutUpdate(BaseModel):
    """Schema para actualizar metadatos de un workout."""
    name: Optional[str] = None
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None


class WorkoutHistory(BaseModel):
    """Datos de resumen de workouts completados para historiales."""
    id: int
    user_id: int
    name: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    template_id: Optional[int] = None

    class Config:
        from_attributes = True


class Workout(WorkoutBase):
    """Representación completa de un workout con ejercicios y metadatos."""
    id: int
    user_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    workout_exercises: List[WorkoutExercise] = []

    class Config:
        from_attributes = True
