"""Operaciones CRUD y utilidades para el modelo `User`.

Este módulo define `CRUDUser`, una especialización de `CRUDBase` con
métodos adicionales como autenticación y borrado en cascada.
"""

from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD específico para el modelo `User`.

    Añade utilidades de autenticación, comprobaciones de permisos y
    operaciones especiales como borrado en cascada.
    """

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Obtener un usuario por su correo electrónico.

        Args:
            db: sesión de base de datos.
            email: correo a buscar.

        Returns:
            Instancia `User` o None si no existe.
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Obtener un usuario por su nombre de usuario (username).

        Args:
            db: sesión de base de datos.
            username: nombre de usuario a buscar.

        Returns:
            Instancia `User` o None si no existe.
        """
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Crear un usuario a partir de un `UserCreate`.

        Hashea la contraseña, crea la entidad y la persiste en la base de datos.

        Args:
            db: sesión de base de datos.
            obj_in: schema con los datos del nuevo usuario.

        Returns:
            La instancia `User` creada.
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Actualizar un usuario.

        Si se proporciona una contraseña en los datos, se hashea antes de
        delegar en `CRUDBase.update`.

        Args:
            db: sesión de base de datos.
            db_obj: instancia existente de `User`.
            obj_in: `UserUpdate` o dict con campos a actualizar.

        Returns:
            La instancia `User` actualizada.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Autenticar un usuario por correo y contraseña.

        Verifica existencia y contraseña. Devuelve la instancia `User`
        si la autenticación es correcta, o None en caso contrario.
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Indica si un usuario está activo."""
        return user.is_active

    def is_admin(self, user: User) -> bool:
        """Indica si un usuario tiene rol de administrador."""
        return user.is_admin

    def delete_with_cascade(self, db: Session, *, user_id: int) -> None:
        """Borra el usuario y todo lo relacionado a él en cascada usando SQLAlchemy."""
        usuario = self.get(db, id=user_id)
        if usuario:
            db.delete(usuario)
            db.commit()


user = CRUDUser(User)
