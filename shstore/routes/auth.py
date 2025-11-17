# shstore/routes/auth.py

from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    session
)

from shstore.models import User
from shstore.utils.security import verify_password

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()

        # usuario no existe o password incorrecta
        if not user or not verify_password(user.password, password):
            return render_template(
                "auth/login.html",
                message="Usuario o contraseña incorrectos",
            )

        # guardar sesión
        session["user_id"] = user.id
        session["role"] = user.role

        return redirect("/admin")

    # GET → mostrar login
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
