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
    #  CARPETA DE IMÁGENES (static/uploads)
    # ================================
    upload_dir = os.path.join(app.static_folder, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = upload_dir
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
    from .routes.files import bp as files_bp   # si quieres eliminarlo luego, se puede

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(files_bp)  # sirve si deseas servir imágenes fuera de /static

    return app
