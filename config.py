# config.py
import os

# Ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ================================
#  CONFIGURACIÓN PARA LOCAL
# ================================
# Cuando trabajas en tu PC, la base está en: instance/dev.db
LOCAL_DB_PATH = os.path.join(BASE_DIR, "instance", "dev.db")


# ================================
#  CONFIGURACIÓN PARA PRODUCCIÓN
# ================================
# En Render definiremos PROD_DB_PATH para usar disco persistente:
#
#    /var/data/dev.db
#
# Si PROD_DB_PATH no existe, usa la base local.
DB_PATH = os.environ.get("PROD_DB_PATH", LOCAL_DB_PATH)


# ================================
#  SQLALCHEMY
# ================================
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
