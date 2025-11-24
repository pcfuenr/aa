"""Base CRUD genérico reutilizable.

Este módulo proporciona `CRUDBase`, una clase genérica que implementa
operaciones CRUD comunes (get, list, create, update, delete) para los
modelos SQLAlchemy del proyecto.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Implementación CRUD genérica.

    Parametrizada por el tipo de modelo y los schemas de creación/actualización.
    """

    def __init__(self, model: Type[ModelType]):
        """Inicializa la clase con el modelo SQLAlchemy objetivo.

        Args:
            model: clase del modelo SQLAlchemy.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Obtener una instancia por su identificador.

        Args:
            db: sesión de base de datos.
            id: identificador de la instancia.

        Returns:
            La instancia o None si no existe.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Listar múltiples instancias con paginación.

        Args:
            db: sesión de base de datos.
            skip: offset.
            limit: número máximo de resultados.

        Returns:
            Lista de instancias del modelo.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Crear y persistir una nueva instancia a partir de un schema.

        Convierte el schema Pydantic a datos serializables, crea la entidad
        y la guarda en la base de datos.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return self._save(db, db_obj)

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Actualizar una instancia existente.

        Acepta un schema Pydantic o un dict; aplica los campos presentes
        y persiste los cambios.
        """
        update_data = self._get_update_data(obj_in)
        db_obj = self._apply_updates(db_obj, update_data)
        return self._save(db, db_obj)

    def _get_update_data(self, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Dict[str, Any]:
        """Normalizar los datos de actualización a un diccionario.

        Si `obj_in` es un dict se devuelve tal cual; si es un schema Pydantic
        se extraen solo los campos seteados.
        """
        if isinstance(obj_in, dict):
            return obj_in
        return obj_in.model_dump(exclude_unset=True)

    def _apply_updates(self, db_obj: ModelType, update_data: Dict[str, Any]) -> ModelType:
        """Aplicar los valores de `update_data` a la instancia.

        Solo se aplican fields que ya existen en el objeto actual.
        """
        obj_data = jsonable_encoder(db_obj)
        for field, value in update_data.items():
            if field in obj_data:
                setattr(db_obj, field, value)
        return db_obj

    def _save(self, db: Session, obj: ModelType) -> ModelType:
        """Persistir el objeto en la base de datos y refrescarlo.

        Devuelve la instancia refrescada desde la DB.
        """
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Eliminar una instancia por id.

        Devuelve la instancia eliminada (o lanza si no existe).
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
