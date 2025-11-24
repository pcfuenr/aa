"""Operaciones CRUD para el modelo `Exercise`.

Contiene `CRUDExercise` con métodos para listar ejercicios activos y por
grupo muscular.
"""

from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    """CRUD específico para ejercicios.

    Proporciona utilidades para obtener ejercicios activos y por grupo muscular.
    """

    def get_active(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Exercise]:
        """Listar ejercicios activos con paginación.

        Args:
            db: sesión de base de datos.
            skip: offset.
            limit: máximo de resultados.

        Returns:
            Lista de `Exercise` activos.
        """
        return (
            db.query(Exercise)
            .filter(Exercise.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_muscle_group(self, db: Session, *, muscle_group: str) -> List[Exercise]:
        """Obtener ejercicios activos por grupo muscular.

        Args:
            db: sesión de base de datos.
            muscle_group: nombre del grupo muscular.

        Returns:
            Lista de `Exercise` que pertenecen al grupo y están activos.
        """
        return (
            db.query(Exercise)
            .filter(Exercise.muscle_group == muscle_group, Exercise.is_active == True)
            .all()
        )


exercise = CRUDExercise(Exercise)
