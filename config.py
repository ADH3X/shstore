# config.py
import os

# =====================================
#  RUTA BASE DEL PROYECTO
# =====================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =====================================
#  BASE DE DATOS (LOCAL vs RENDER)
# =====================================
# En tu PC la base está en: ./instance/dev.db
LOCAL_DB_PATH = os.path.join(BASE_DIR, "instance", "dev.db")

# En Render usarás un disco persistente, por ejemplo:
#   /var/data/dev.db
# y lo apuntas con la variable de entorno PROD_DB_PATH
DB_PATH = os.environ.get("PROD_DB_PATH", LOCAL_DB_PATH)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# =====================================
#  CARPETA DE IMÁGENES (UPLOADS)
# =====================================
# En local usas la carpeta del proyecto:
#   ./shstore/static/uploads
LOCAL_UPLOAD_FOLDER = os.path.join(BASE_DIR, "shstore", "static", "uploads")

# En Render, las imágenes van al disco persistente:
#   /var/data/uploads  (lo pones en la env PROD_UPLOAD_FOLDER)
UPLOAD_FOLDER = os.environ.get("PROD_UPLOAD_FOLDER", LOCAL_UPLOAD_FOLDER)
