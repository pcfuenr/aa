set -e
#Trae el main para poder entrar a el
export PYTHONPATH=/workouts_udec_backend

# Esperar a que Postgres esté listo
until pg_isready -h "$POSTGRES_SERVER" -U "$POSTGRES_USER"; do
  echo "Esperando a que la base de datos esté disponible..."
  sleep 2
done

# Generar migración inicial solo si no hay archivos en alembic/versions
if [ -z "$(ls -A alembic/versions)" ]; then
  alembic revision --autogenerate -m "Initial migration"
fi

alembic upgrade head
python create_admin.py
python app/main.py

