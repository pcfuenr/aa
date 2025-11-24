"""Importa los modelos para registrar la metadata de SQLAlchemy.

Este módulo se usa por Alembic y otras utilidades que necesitan `Base.metadata`.
"""

from app.db.base_class import Base
from app.models.user import User
from app.models.exercise import Exercise
from app.models.workout import (
    Workout,
    WorkoutExercise,
    ExerciseSet,
    WorkoutTemplate,
    WorkoutTemplateExercise,
)
