import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ================================
    #  CONFIGURACIÓN GENERAL
    # ================================
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # Base de datos (local o Render)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    # ================================
    #  CONFIGURAR CARPETA PERSISTENTE
    #  PARA GUARDAR IMÁGENES
    # ================================
    PERSISTENT_UPLOAD_DIR = "/var/data/uploads"
    os.makedirs(PERSISTENT_UPLOAD_DIR, exist_ok=True)

    # Flask usará este folder
    app.config["UPLOAD_FOLDER"] = PERSISTENT_UPLOAD_DIR
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4MB máx por imagen

    # ================================
    #  INICIALIZAR BASE DE DATOS
    # ================================
    db.init_app(app)

    # Importar modelos para que SQLAlchemy los registre
    from . import models  # noqa

    # ================================
    #  BLUEPRINTS DE TODAS LAS RUTAS
    # ================================
    from .routes.public import bp as public_bp
    from .routes.auth import bp as auth_bp
    from .routes.admin import bp as admin_bp
    from .routes.cart import bp as cart_bp
    from .routes.files import bp as files_bp   # <--- NUEVO Y NECESARIO

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(files_bp)           # <--- REGISTRA RUTA /uploads/

    return app
