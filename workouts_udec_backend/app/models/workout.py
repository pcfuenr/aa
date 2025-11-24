"""Modelos relacionados con workouts, plantillas y sets.

Contiene:
- WorkoutTemplate: plantilla reutilizable con ejercicios sugeridos.
- WorkoutTemplateExercise: relación plantilla<->ejercicio con sugerencias.
- Workout: sesión concreta del usuario basada opcionalmente en plantilla.
- WorkoutExercise: ejercicio dentro de un workout.
- ExerciseSet: sets individuales dentro de un workout exercise.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Float,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class WorkoutTemplate(Base):
    """Plantilla de entrenamiento que agrupa ejercicios sugeridos."""

    __tablename__ = "workout_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator = relationship("User", back_populates="templates")
    template_exercises = relationship(
        "WorkoutTemplateExercise",
        back_populates="template",
        cascade="all, delete-orphan",
    )


class WorkoutTemplateExercise(Base):
    """Asocia un ejercicio a una plantilla con sugerencias (sets, reps...)."""

    __tablename__ = "workout_template_exercises"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("workout_templates.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    suggested_sets = Column(Integer, nullable=True)
    suggested_reps = Column(Integer, nullable=True)
    suggested_weight = Column(Float, nullable=True)
    suggested_duration = Column(Integer, nullable=True)  # in seconds

    template = relationship("WorkoutTemplate", back_populates="template_exercises")
    exercise = relationship("Exercise")


class Workout(Base):
    """Instancia de sesión de entrenamiento para un usuario."""

    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    template_id = Column(Integer, ForeignKey("workout_templates.id"), nullable=True)

    user = relationship("User", back_populates="workouts")
    template = relationship("WorkoutTemplate")
    workout_exercises = relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )


class WorkoutExercise(Base):
    """Ejercicio específico dentro de un workout."""

    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise")
    sets = relationship(
        "ExerciseSet", back_populates="workout_exercise", cascade="all, delete-orphan"
    )


class ExerciseSet(Base):
    """Set individual de un ejercicio dentro de un workout (reps, peso...)."""

    __tablename__ = "exercise_sets"

    id = Column(Integer, primary_key=True, index=True)
    workout_exercise_id = Column(
        Integer, ForeignKey("workout_exercises.id"), nullable=False
    )
    set_number = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    rest_duration = Column(Integer, nullable=True)  # in seconds
    completed = Column(Boolean, default=False)

    workout_exercise = relationship("WorkoutExercise", back_populates="sets")
