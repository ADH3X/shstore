# shstore/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # ------------------------------
    # CONFIG BÁSICA
    # ------------------------------
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///dev.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ------------------------------
    # CONFIG DE SUBIDA DE IMÁGENES
    # (usa static/uploads)
    # ------------------------------
    upload_folder = os.path.join(app.root_path, "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = upload_folder
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024   # 4MB

    # ------------------------------
    # INICIALIZAR BD
    # ------------------------------
    db.init_app(app)

    # Importar modelos para que SQLAlchemy los registre
    from . import models  # noqa

    # ------------------------------
    # BLUEPRINTS
    # ------------------------------
    from .routes.public import bp as public_bp
    from .routes.auth import bp as auth_bp
    from .routes.admin import bp as admin_bp
    from .routes.cart import bp as cart_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)

    return app
