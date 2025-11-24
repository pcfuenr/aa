"""Clase base declarativa para modelos SQLAlchemy.

Define una `Base` con comportamiento por defecto para tablename.
"""

from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Clase base para todos los modelos; añade un id y nombre de tabla automático."""
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self, cls) -> str:
        """Genera el nombre de la tabla a partir del nombre de la clase en minúsculas."""
        return cls.__name__.lower()
