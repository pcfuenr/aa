"""Router principal que incluye los routers de los endpoints de la API.

Este módulo centraliza la inclusión de los routers de autenticación,
usuarios, ejercicios, workouts, administración y health checks.
"""

from fastapi import APIRouter
from app.api.endpoints import auth, users, exercises, workouts, admin, health

# Router principal que se monta en la aplicación FastAPI
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
