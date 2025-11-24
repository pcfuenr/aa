"""Funciones de seguridad: hash de contraseñas y creación de tokens JWT.

Este módulo encapsula la creación/verificación de contraseñas y la
generación de access tokens JWT usados por la API.
"""

from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Crear un JWT de acceso para un sujeto dado.

    Args:
        subject: identidad del sujeto (usualmente user id o email).
        expires_delta: expiración opcional; si no se entrega se usa la
            configuración `ACCESS_TOKEN_EXPIRE_MINUTES`.

    Returns:
        Token JWT codificado como string.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar que una contraseña en texto plano coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generar el hash seguro para una contraseña.

    Usa `passlib` con el esquema configurado (`bcrypt`).
    """
    return pwd_context.hash(password)
