# create_users.py
from app import app
from shstore.models import db, User
from werkzeug.security import generate_password_hash


def create_user(username: str, raw_password: str, role: str = "admin"):
    with app.app_context():
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"El usuario '{username}' ya existe, no se crea de nuevo.")
            return

        user = User(
            username=username,
            password=generate_password_hash(raw_password),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        print(f"Usuario '{username}' creado correctamente.")


if __name__ == "__main__":
    # puedes cambiar las contraseñas si quieres
    create_user("diego", "Diego2025!")
    create_user("adhex", "Adhex2025!")
