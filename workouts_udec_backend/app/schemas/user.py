"""Schemas Pydantic para usuarios y tokens.

Contiene modelos para creación, actualización y representación de usuarios,
así como los esquemas de token usados en la autenticación.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Modelo base con los campos que puede tener un usuario."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    """Schema para crear un usuario nuevo (requiere email, username y password)."""
    email: EmailStr
    username: str
    password: str


class UserUpdate(UserBase):
    """Schema para actualizar datos de usuario (actualización parcial)."""
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """Campos adicionales presentes cuando el usuario está persistido en DB."""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """Schema público que representa un usuario expuesto por la API."""
    pass


class UserInDB(UserInDBBase):
    """Modelo interno que incluye la contraseña hasheada almacenada en DB."""
    hashed_password: str


class Token(BaseModel):
    """Schema para el token de acceso (JWT) devuelto por el endpoint de login."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Payload esperado dentro del token JWT (información mínima)."""
    sub: Optional[int] = None
