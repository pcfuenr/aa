"""Punto de entrada de la API FastAPI del proyecto (rutas principales)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.main_router import api_router

app = FastAPI(
    title="Workout Tracker API",
    description="FastAPI backend for workout tracking application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Health check simple que devuelve el estado del servicio.

    Devuelve: dict con clave 'status'.
    """
    return {"status": "ok"}


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
