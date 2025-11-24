"""Configuración de la aplicación basada en Pydantic Settings.

Define la clase `Settings` que carga variables de entorno y expone
valores de configuración usados por la aplicación (secret key, DB, tokens...).
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Ajustes de aplicación cargados desde variables de entorno.

    Valores por defecto están definidos para desarrollo; en producción
    debe sobrescribirse mediante variables de entorno o un archivo `.env`.
    """
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_DB: str = "workouts_db"
    DATABASE_URL: Optional[str] = None

    @property
    def database_url(self) -> str:
        """Construir y devolver la URL de conexión a la base de datos.

        Si `DATABASE_URL` está definida se devuelve tal cual; de lo
        contrario se construye la URL a partir de los parámetros.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    class Config:
        """Configuración interna de Pydantic Settings.

        Aquí se configura el archivo `.env` por defecto.
        """
        env_file = ".env"


settings = Settings()
