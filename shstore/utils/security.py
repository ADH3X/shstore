# shstore/utils/security.py

from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------------------
#  PASSWORD SECURITY
# ---------------------------

def hash_password(password: str) -> str:
    """Genera un hash seguro para contraseñas."""
    return generate_password_hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return check_password_hash(hashed_password, password)


# ---------------------------
#  ROUTE PROTECTION
# ---------------------------

def login_required(view_func):
    """
    Protege rutas que requieren estar logueado.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debe iniciar sesión para acceder.", "danger")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Protege rutas exclusivas para administradores.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            flash("Acceso restringido solo para administradores.", "danger")
            return redirect(url_for("public.home"))
        return view_func(*args, **kwargs)
    return wrapper
