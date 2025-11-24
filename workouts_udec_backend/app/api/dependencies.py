"""Dependencias de FastAPI utilizadas por los routers.

Contiene dependencias para obtener la sesión de DB y resolver el usuario
autenticado/activo/administrador a partir del token JWT.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.crud.crud_user import user

security_scheme = HTTPBearer()


def get_db() -> Generator:
    """Dependencia que provee una sesión de base de datos y la cierra.

    Uso típico en endpoints: `db: Session = Depends(get_db)`.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(security_scheme)
) -> User:
    """Resolver el usuario actual desde el token JWT.

    Decodifica el token, obtiene el `sub` (user id) y carga la entidad
    `User` desde la base de datos. Lanza HTTPException si no es válido.
    """
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        user_id: int = payload.get("sub")
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Verificar que el usuario actual esté activo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Verificar que el usuario actual tenga privilegios de administrador."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
