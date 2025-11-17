# shstore/routes/cart.py
from flask import Blueprint

# Blueprint del carrito
bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.route("/")
def view_cart():
    # Por ahora solo un placeholder.
    # Más adelante acá mostraremos los productos agregados al carrito.
    return "Carrito en construcción"
