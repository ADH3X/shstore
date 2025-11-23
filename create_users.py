# create_users.py
from shstore import create_app, db
from shstore.models import User
from werkzeug.security import generate_password_hash


def main():
    app = create_app()

    with app.app_context():
        # 1) Borrar usuario "admin" viejo si existe
        old_admin = User.query.filter_by(username="admin").first()
        if old_admin:
            print("Eliminando usuario 'admin' anterior...")
            db.session.delete(old_admin)
            db.session.commit()

        # 2) Borrar versiones viejas de diego/adhex si las hubiera
        for username in ("diego", "adhex"):
            exists = User.query.filter_by(username=username).first()
            if exists:
                print(f"Eliminando usuario viejo '{username}'...")
                db.session.delete(exists)
        db.session.commit()

        # 3) Crear usuarios oficiales
        diego = User(
            username="diego",
            password=generate_password_hash("Diego2025*"),
            role="admin",
        )
        adhex = User(
            username="adhex",
            password=generate_password_hash("Adhex2025*"),
            role="admin",
        )

        db.session.add_all([diego, adhex])
        db.session.commit()

        print("Usuarios creados correctamente:")
        print(" - diego  /  Diego2025*  (role=admin)")
        print(" - adhex  /  Adhex2025*  (role=admin)")


if __name__ == "__main__":
    main()
