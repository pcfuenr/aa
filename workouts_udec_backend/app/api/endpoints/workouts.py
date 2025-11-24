"""Rutas para gestionar workouts y su seguimiento.

Incluye creación desde plantillas, gestión de ejercicios y sets, historial
y comprobaciones de permisos/propiedad.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.sql import func

from app.api import dependencies
from app.crud.crud_workout import workout, workout_template
from app.models.user import User
from app.schemas.workout import (
    Workout as WorkoutSchema,
    WorkoutHistory as WorkoutHistorySchema,
    WorkoutCreate,
    WorkoutUpdate,
    WorkoutTemplate as WorkoutTemplateSchema,
    WorkoutExercise as WorkoutExerciseSchema,
    WorkoutExerciseCreate,
    ExerciseSet as ExerciseSetSchema,
    ExerciseSetCreate,
    ExerciseSetUpdate,
)

router = APIRouter()


def validate_workout_access(
    db: Session, workout_id: int, current_user: User, allow_completed: bool = False
):
    """Validar permisos y existencia de un workout.

    Comprueba que el workout existe, pertenece al usuario actual y si está
    permitido modificarlo (no completado) según `allow_completed`.
    """
    workout_obj = workout.get(db, id=workout_id)
    if not workout_obj:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not allow_completed and workout_obj.completed_at:
        raise HTTPException(status_code=400, detail="Cannot modify completed workout")
    return workout_obj


@router.get("/templates", response_model=List[WorkoutTemplateSchema])
def read_workout_templates(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Listar plantillas públicas de entrenamiento con paginación."""
    # Get all templates with exercises and filter for public ones
    all_templates = workout_template.get_multi_with_exercises(
        db, skip=0, limit=1000
    )  # Get more to allow proper filtering
    public_templates = [t for t in all_templates if t.is_public]

    # Apply pagination to filtered results
    start_idx = skip
    end_idx = skip + limit
    return public_templates[start_idx:end_idx]


@router.get("/templates/{template_id}", response_model=WorkoutTemplateSchema)
def read_workout_template(
    *,
    db: Session = Depends(dependencies.get_db),
    template_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Obtener una plantilla por id si es pública o es del usuario."""
    template = workout_template.get_with_exercises(db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if not template.is_public and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return template


@router.post("/templates/{template_id}/create-workout", response_model=WorkoutSchema)
def create_workout_from_template(
    *,
    db: Session = Depends(dependencies.get_db),
    template_id: int,
    workout_in: WorkoutCreate,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Crear un workout a partir de una plantilla pública o propia."""
    template = workout_template.get_with_exercises(db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if not template.is_public and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Create workout with template data
    workout_data = {
        "name": workout_in.name or template.name,
        "notes": workout_in.notes,
        "template_id": template_id,
        "user_id": current_user.id,
    }

    return workout.create_from_template(
        db, template=template, workout_data=workout_data
    )


@router.get("/", response_model=List[WorkoutSchema])
def read_workouts(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Listar workouts del usuario autenticado."""
    workouts = workout.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return workouts


@router.get("/active", response_model=WorkoutSchema)
def get_active_workout(
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Obtener el workout activo del usuario, si existe."""
    active_workout = workout.get_active_by_user(db, user_id=current_user.id)
    if not active_workout:
        raise HTTPException(status_code=404, detail="No active workout found")
    return active_workout


@router.post("/", response_model=WorkoutSchema)
def create_workout(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_in: WorkoutCreate,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Crear un nuevo workout para el usuario (si no tiene activo)."""
    # Check if user has an active workout
    active_workout = workout.get_active_by_user(db, user_id=current_user.id)
    if active_workout:
        raise HTTPException(
            status_code=400,
            detail="You already have an active workout. Complete it before starting a new one.",
        )

    workout_data = workout_in.dict()
    workout_data["user_id"] = current_user.id
    workout_obj = workout.create(db, obj_in=workout_data)
    return workout_obj


@router.put("/{workout_id}", response_model=WorkoutSchema)
def update_workout(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    workout_in: WorkoutUpdate,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Actualizar un workout (permite marcar completado)."""
    workout_obj = validate_workout_access(
        db, workout_id, current_user, allow_completed=True
    )
    return workout.update(db, db_obj=workout_obj, obj_in=workout_in)


@router.put("/{workout_id}/complete")
def complete_workout(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Marcar un workout como completado."""
    workout_obj = validate_workout_access(
        db, workout_id, current_user, allow_completed=True
    )
    if workout_obj.completed_at:
        raise HTTPException(status_code=400, detail="Workout already completed")
    workout.update(db, db_obj=workout_obj, obj_in={"completed_at": func.now()})
    return {"message": "Workout completed successfully"}


@router.delete("/{workout_id}")
def cancel_workout(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Cancelar y eliminar un workout (si no está completado)."""
    workout_obj = validate_workout_access(db, workout_id, current_user)
    if workout_obj.completed_at:
        raise HTTPException(status_code=400, detail="Cannot cancel a completed workout")
    workout.cancel_workout(db, workout_id=workout_id)
    return {"message": "Workout cancelled and removed successfully"}


@router.get("/history", response_model=List[WorkoutSchema])
def get_workout_history(
    *,
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Obtener el historial de workouts completados del usuario."""
    completed_workouts = workout.get_completed_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return completed_workouts


@router.get("/{workout_id}", response_model=WorkoutSchema)
def read_workout(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Obtener un workout por id verificando propiedad y permisos."""
    workout_obj = workout.get(db, id=workout_id)
    if not workout_obj:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return workout_obj


# Exercise tracking within workouts
@router.post("/{workout_id}/exercises", response_model=WorkoutExerciseSchema)
def add_exercise_to_workout(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    exercise_in: WorkoutExerciseCreate,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Agregar un ejercicio a un workout (usuario propietario)."""
    workout_obj = validate_workout_access(db, workout_id, current_user)

    return workout.add_exercise_to_workout(
        db, workout_id=workout_id, exercise_data=exercise_in
    )


@router.post(
    "/{workout_id}/exercises/{exercise_id}/sets", response_model=ExerciseSetSchema
)
def add_set_to_exercise(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    exercise_id: int,
    set_in: ExerciseSetCreate,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Añadir un set a un ejercicio dentro de un workout."""
    _ = validate_workout_access(db, workout_id, current_user)
    try:
        return workout.add_set_to_exercise(
            db, workout_id=workout_id, exercise_id=exercise_id, set_data=set_in
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{workout_id}/exercises/{exercise_id}/sets/{set_id}",
    response_model=ExerciseSetSchema,
)
def update_exercise_set(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    exercise_id: int,
    set_id: int,
    set_in: ExerciseSetUpdate,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Actualizar un set de ejercicio dentro de un workout."""
    _ = validate_workout_access(db, workout_id, current_user)
    try:
        return workout.update_exercise_set(
            db,
            workout_id=workout_id,
            exercise_id=exercise_id,
            set_id=set_id,
            set_data=set_in,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{workout_id}/exercises/{exercise_id}/sets/{set_id}")
def delete_exercise_set(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    exercise_id: int,
    set_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Eliminar un set de ejercicio dentro de un workout."""
    _ = validate_workout_access(db, workout_id, current_user)
    try:
        workout.delete_exercise_set(
            db,
            workout_id=workout_id,
            exercise_id=exercise_id,
            set_id=set_id,
        )
        return {"message": "Exercise set deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Progression tracking
@router.get("/{workout_id}/progression/{exercise_id}")
def get_exercise_progression(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    exercise_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Obtener datos de progresión para un ejercicio específico."""
    progression_data = workout.get_exercise_progression(
        db, user_id=current_user.id, exercise_id=exercise_id, limit=10
    )

    return {"exercise_id": exercise_id, "progression": progression_data}


# Comments/Notes system
@router.put("/{workout_id}/notes")
def update_workout_notes(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    notes_data: dict,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Actualizar las notas de un workout."""
    workout_obj = validate_workout_access(db, workout_id, current_user)
    workout.update(
        db,
        db_obj=workout_obj,
        obj_in={"notes": notes_data.get("notes")},
    )
    return {"message": "Workout notes updated successfully"}


@router.put(
    "/{workout_id}/exercises/{exercise_id}/notes", response_model=WorkoutExerciseSchema
)
def update_exercise_notes(
    *,
    db: Session = Depends(dependencies.get_db),
    workout_id: int,
    exercise_id: int,
    notes_data: dict,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """Actualizar notas de un ejercicio dentro de un workout."""
    _ = validate_workout_access(db, workout_id, current_user)
    try:
        return workout.update_exercise_notes(
            db,
            workout_id=workout_id,
            exercise_id=exercise_id,
            notes=notes_data.get("notes", ""),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
