# shstore/routes/public.py
from flask import Blueprint, render_template, request
from shstore.models import Product, Category
from shstore.utils.whatsapp import (
    WHATSAPP_CONTACT_1,
    WHATSAPP_CONTACT_2,
    format_whatsapp_message,
    whatsapp_link,
)

bp = Blueprint("public", __name__)

# mismas categorías que usas en admin
CATEGORY_OPTIONS = [
    ("zapatillas", "Zapatillas"),
    ("poleras", "Poleras / Remeras"),
    ("buzos", "Buzos / Hoodies"),
    ("camperas", "Camperas / Abrigos"),
    ("camisas", "Camisas"),
    ("pantalones", "Pantalones"),
    ("shorts", "Shorts"),
    ("conjuntos", "Conjuntos"),
    ("accesorios", "Accesorios"),
    ("ropa-interior", "Ropa interior"),
    ("bolsos", "Bolsos / Mochilas"),
    ("outlet", "Outlet"),
    ("nuevos", "Nuevos ingresos"),
    # nueva categoría especial
    ("joyitas-cumavi", "Joyitas Cumavi"),
    ("gorras", "Gorras"),
]


@bp.route("/")
def home():
    q = request.args.get("q", "").strip()
    category_slug = request.args.get("category", "").strip()

    query = Product.query

    # ---- filtro por categoría / estado especial ----
    if category_slug:
        if category_slug == "joyitas-cumavi":
            # Filtra por estado especial
            query = query.filter(Product.condition == "Joyitas Cumavi")
        else:
            # Categorías normales usando la tabla Category
            cat = Category.query.filter_by(slug=category_slug).first()
            if cat:
                query = query.filter(Product.category_id == cat.id)
            else:
                # slug inválido -> no devuelve nada
                query = query.filter(False)

    # ---- filtro por búsqueda ----
    if q:
        like = f"%{q}%"
        query = query.filter(Product.name.ilike(like))

    products = query.order_by(Product.created_at.desc()).all()

    # ---- recomendaciones cuando NO hay resultados ----
    recommended_products = []
    if not products:
        fallback_query = Product.query

        if category_slug:
            if category_slug == "joyitas-cumavi":
                # Si no hay joyitas, recomienda otras joyitas
                fallback_query = fallback_query.filter(
                    Product.condition == "Joyitas Cumavi"
                )
            else:
                # recomendaciones dentro de la misma categoría normal
                cat_for_rec = Category.query.filter_by(slug=category_slug).first()
                if cat_for_rec:
                    fallback_query = fallback_query.filter(
                        Product.category_id == cat_for_rec.id
                    )

        recommended_products = (
            fallback_query
            .order_by(Product.created_at.desc())
            .limit(8)
            .all()
        )

    return render_template(
        "home.html",
        products=products,
        recommended_products=recommended_products,
        q=q,
        category_filter=category_slug,
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/products/<slug>")
def product_detail(slug: str):
    # ---------- PRODUCTO PRINCIPAL ----------
    product = Product.query.filter_by(slug=slug).first_or_404()

    # ---------- GALERÍA DE IMÁGENES ----------
    images: list[str] = []
    usados = set()

    if product.image_url:
        images.append(product.image_url)
        usados.add(product.image_url)

    for img in product.images:
        if img.image_url and img.image_url not in usados:
            images.append(img.image_url)
            usados.add(img.image_url)

    # ---------- PRODUCTOS RELACIONADOS ----------
    related_query = Product.query.filter(Product.id != product.id)
    if product.category_id:
        related_query = related_query.filter(
            Product.category_id == product.category_id
        )

    related_products = (
        related_query.order_by(Product.created_at.desc()).limit(6).all()
    )

    # ---------- WHATSAPP ----------
    msg = format_whatsapp_message(product.name, float(product.price))
    wa_link_1 = whatsapp_link(WHATSAPP_CONTACT_1, msg)
    wa_link_2 = whatsapp_link(WHATSAPP_CONTACT_2, msg)

    return render_template(
        "products/detail.html",
        product=product,
        images=images,
        related_products=related_products,
        wa_link_1=wa_link_1,
        wa_link_2=wa_link_2,
    )
