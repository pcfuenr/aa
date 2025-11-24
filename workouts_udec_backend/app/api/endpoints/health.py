"""Endpoint de health check simple.

Proporciona una ruta ligera para comprobar que la API está respondiendo.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check():
    """Devolver estado de salud de la aplicación."""
    return {"status": "ok"}
