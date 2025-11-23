# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ruta local por defecto (cuando trabajas en tu PC)
LOCAL_DB_PATH = os.path.join(BASE_DIR, "..", "instance", "dev.db")

# En producción usarás la variable de entorno PROD_DB_PATH
DB_PATH = os.environ.get("PROD_DB_PATH", LOCAL_DB_PATH)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
