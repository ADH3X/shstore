# shstore/routes/admin.py
import os
import re
import time

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER  # ⬅️ NUEVO

from shstore.models import db, Product, Category, ProductImage
from shstore.utils.security import login_required, admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")



# --- LISTAS PARA SELECTS --- #
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
    ("ropa-interior", "Ropa Interior"),
    ("bolsos", "Bolsos / Mochilas"),
    ("outlet", "Outlet"),
    ("nuevos", "Nuevos ingresos"),
    ("joyitas-cumavi", "Joyitas Cumavi"),
    ("gorras", "Gorras"),
]

GENDER_OPTIONS = ["Hombre", "Mujer", "Unisex", "Niño", "Niña"]

CONDITION_OPTIONS = [
    "Joyitas Cumavi",
    "Nuevo",
    "Como nuevo",
    "Muy bueno",
    "Bueno",
    "Con detalles"
]

COLOR_OPTIONS = [
    "Negro", "Blanco", "Gris", "Azul", "Rojo",
    "Verde", "Amarillo", "Rosa", "Beige", "Marrón",
    "Morado", "Naranja"
]

SIZE_CLOTHES_OPTIONS = [
    "XS", "S", "M", "L", "XL", "XXL"
]

SIZE_SHOES_OPTIONS = [str(n) for n in range(34, 46)]  # 34 a 45

MATERIAL_OPTIONS = [
    "Algodón", "Poliéster", "Cuero", "Sintético",
    "Lana", "Denim", "Lino"
]


# ------------------ HELPERS ------------------ #

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def make_slug(name: str) -> str:
    """
    Slug sencillo: "Campera negra básica" -> "campera-negra-basica"
    (para productos)
    """
    base = name.lower().strip()
    base = re.sub(r"[^a-z0-9áéíóúñ ]", "", base)
    base = base.replace(" ", "-")
    slug = re.sub(r"-+", "-", base)

    exists = Product.query.filter_by(slug=slug).first()
    if exists:
        slug = f"{slug}-{int(time.time())}"

    return slug


def make_category_slug(name: str) -> str:
    """
    Slug para categorías.
    """
    base = name.lower().strip()
    base = re.sub(r"[^a-z0-9áéíóúñ ]", "", base)
    base = base.replace(" ", "-")
    slug = re.sub(r"-+", "-", base)

    exists = Category.query.filter_by(slug=slug).first()
    if exists:
        slug = f"{slug}-{int(time.time())}"

    return slug


def get_or_create_category(slug: str) -> Category | None:
    """
    Recibe el slug que viene del <select> (zapatillas, camperas-abrigos, etc.)
    y devuelve un objeto Category. Si no existe, lo crea.
    """
    slug = (slug or "").strip()
    if not slug:
        return None

    # 1) Buscar por slug
    cat = Category.query.filter_by(slug=slug).first()
    if cat:
        return cat

    # 2) Si no existe, generamos un nombre bonito a partir del slug
    #    zapatillas -> "Zapatillas"
    #    ropa-interior -> "Ropa Interior"
    nice_name = slug.replace("-", " ").title()

    cat = Category(name=nice_name, slug=slug)
    db.session.add(cat)
    db.session.flush()  # para tener cat.id inmediatamente
    return cat


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def save_image_file(file_storage):
    """
    Guarda la imagen en la carpeta de uploads (local o disco persistente)
    y devuelve la ruta relativa (ej: 'uploads/campera-123456.png')
    o None si algo falla.
    """
    if not file_storage or file_storage.filename == "":
        return None

    if not allowed_file(file_storage.filename):
        return None

    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    base_name = filename.rsplit(".", 1)[0]
    final_name = f"{base_name}-{int(time.time())}.{ext}"

    # Usa UPLOAD_FOLDER de config; si en app.config hay uno, tiene prioridad
    upload_folder = current_app.config.get("UPLOAD_FOLDER", UPLOAD_FOLDER)
    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, final_name)
    file_storage.save(save_path)

    # Lo que guardamos en la BD
    return f"uploads/{final_name}"


# ------------------ VISTAS ADMIN ------------------ #

@bp.route("/")
@login_required
@admin_required
def dashboard():
    total_products = Product.query.count()
    return render_template("admin/dashboard.html", total_products=total_products)


@bp.route("/products")
@login_required
@admin_required
def products_list():
    q = request.args.get("q", "", type=str).strip()

    query = Product.query
    if q:
        like = f"%{q}%"
        # Busca por nombre y slug
        from sqlalchemy import or_
        query = query.filter(
            or_(
                Product.name.ilike(like),
                Product.slug.ilike(like),
            )
        )

    products = query.order_by(Product.created_at.desc()).all()
    return render_template("admin/products_list.html", products=products, q=q)


@bp.route("/products/new", methods=["GET", "POST"])
@login_required
@admin_required
def product_create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price_raw = request.form.get("price", "0").strip()
        category_slug = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        # selects nuevos (pueden venir vacíos)
        gender       = request.form.get("gender") or None
        condition    = request.form.get("condition") or None
        color        = request.form.get("color") or None
        size_clothes = request.form.get("size_clothes") or None
        size_shoes   = request.form.get("size_shoes") or None
        material     = request.form.get("material") or None
        color_detail = request.form.get("color_detail", "").strip() or None

        # --- precio ---
        try:
            price = float(price_raw.replace(",", "."))
        except ValueError:
            price = 0.0

        if not name:
            flash("El nombre es obligatorio.", "error")
            return render_template(
                "admin/products_form.html",
                product=None,
                gender_options=GENDER_OPTIONS,
                condition_options=CONDITION_OPTIONS,
                color_options=COLOR_OPTIONS,
                size_clothes_options=SIZE_CLOTHES_OPTIONS,
                size_shoes_options=SIZE_SHOES_OPTIONS,
                material_options=MATERIAL_OPTIONS,
                category_options=CATEGORY_OPTIONS,
            )

        slug = make_slug(name)

        # categoría -> objeto Category (o None)
        category_obj = get_or_create_category(category_slug)

        # varias imágenes (máx 6)
        image_files = request.files.getlist("images")
        image_files = [f for f in image_files if f and f.filename]

        saved_paths = []
        for f in image_files[:6]:
            path = save_image_file(f)
            if path:
                saved_paths.append(path)

        cover = saved_paths[0] if saved_paths else None

        product = Product(
            name=name,
            slug=slug,
            price=price,
            description=description,
            image_url=cover,
            category_id=category_obj.id if category_obj else None,
            gender=gender,
            condition=condition,
            color=color,
            size_clothes=size_clothes,
            size_shoes=size_shoes,
            material=material,
            color_detail=color_detail,
        )
        # por si quieres también la relación en memoria:
        product.category = category_obj

        db.session.add(product)
        db.session.flush()  # para tener product.id

        for pos, path in enumerate(saved_paths):
            db.session.add(
                ProductImage(
                    product_id=product.id,
                    image_url=path,
                    position=pos,
                )
            )

        db.session.commit()
        flash("Producto creado correctamente.", "success")
        return redirect(url_for("admin.products_list"))

    # GET → form vacío
    return render_template(
        "admin/products_form.html",
        product=None,
        gender_options=GENDER_OPTIONS,
        condition_options=CONDITION_OPTIONS,
        color_options=COLOR_OPTIONS,
        size_clothes_options=SIZE_CLOTHES_OPTIONS,
        size_shoes_options=SIZE_SHOES_OPTIONS,
        material_options=MATERIAL_OPTIONS,
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price_raw = request.form.get("price", "0").strip()
        category_slug = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        gender       = request.form.get("gender") or None
        condition    = request.form.get("condition") or None
        color        = request.form.get("color") or None
        size_clothes = request.form.get("size_clothes") or None
        size_shoes   = request.form.get("size_shoes") or None
        material     = request.form.get("material") or None
        color_detail = request.form.get("color_detail", "").strip() or None

        # --- precio ---
        try:
            price = float(price_raw.replace(",", "."))
        except ValueError:
            price = 0.0

        if not name:
            flash("El nombre es obligatorio.", "error")
            return render_template(
                "admin/products_form.html",
                product=product,
                gender_options=GENDER_OPTIONS,
                condition_options=CONDITION_OPTIONS,
                color_options=COLOR_OPTIONS,
                size_clothes_options=SIZE_CLOTHES_OPTIONS,
                size_shoes_options=SIZE_SHOES_OPTIONS,
                material_options=MATERIAL_OPTIONS,
                category_options=CATEGORY_OPTIONS,
            )

        # slug solo cambia si cambia el nombre
        if name != product.name:
            product.slug = make_slug(name)

        product.name = name
        product.price = price
        product.description = description

        # actualizar filtros básicos
        product.gender       = gender
        product.condition    = condition
        product.color        = color
        product.size_clothes = size_clothes
        product.size_shoes   = size_shoes
        product.material     = material
        product.color_detail = color_detail

        # 🔹 categoría como OBJETO + FK explícita
        category_obj = get_or_create_category(category_slug)
        if category_obj:
            product.category_id = category_obj.id
            product.category = category_obj
        else:
            product.category_id = None
            product.category = None

        # -----------------------------
        # 1) ELIMINAR IMÁGENES MARCADAS
        # -----------------------------
        delete_ids_raw = request.form.getlist("delete_image_ids")
        delete_ids = [int(x) for x in delete_ids_raw if x.isdigit()]

        deleted_paths = set()
        if delete_ids:
            images_to_delete = (
                ProductImage.query
                .filter(
                    ProductImage.product_id == product.id,
                    ProductImage.id.in_(delete_ids),
                )
                .all()
            )
            for img in images_to_delete:
                deleted_paths.add(img.image_url)
                db.session.delete(img)

        # -----------------------------
        # 2) SUBIR NUEVAS IMÁGENES
        # -----------------------------
        remaining_after_delete = (
            ProductImage.query
            .filter(
                ProductImage.product_id == product.id,
                ~ProductImage.id.in_(delete_ids),
            )
            .count()
        )

        max_extra = max(0, 6 - remaining_after_delete)

        image_files = request.files.getlist("images")
        image_files = [f for f in image_files if f and f.filename][:max_extra]

        new_paths = []
        for f in image_files:
            path = save_image_file(f)
            if path:
                new_paths.append(path)

        db.session.flush()  # aseguramos IDs

        remaining = (
            ProductImage.query
            .filter(ProductImage.product_id == product.id)
            .order_by(ProductImage.position.asc(), ProductImage.id.asc())
            .all()
        )

        for idx, img in enumerate(remaining):
            img.position = idx
        start_pos = len(remaining)

        for i, path in enumerate(new_paths):
            db.session.add(
                ProductImage(
                    product_id=product.id,
                    image_url=path,
                    position=start_pos + i,
                )
            )

        # -----------------------------
        # 3) AJUSTAR PORTADA (image_url)
        # -----------------------------
        if product.image_url in deleted_paths:
            product.image_url = None

        if not product.image_url:
            first_img = (
                ProductImage.query
                .filter(ProductImage.product_id == product.id)
                .order_by(ProductImage.position.asc(), ProductImage.id.asc())
                .first()
            )
            if first_img:
                product.image_url = first_img.image_url

        db.session.commit()
        flash("Producto actualizado.", "success")
        return redirect(url_for("admin.product_edit", product_id=product.id))

    # GET
    return render_template(
        "admin/products_form.html",
        product=product,
        gender_options=GENDER_OPTIONS,
        condition_options=CONDITION_OPTIONS,
        color_options=COLOR_OPTIONS,
        size_clothes_options=SIZE_CLOTHES_OPTIONS,
        size_shoes_options=SIZE_SHOES_OPTIONS,
        material_options=MATERIAL_OPTIONS,
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
@admin_required
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Producto eliminado.", "success")
    return redirect(url_for("admin.products_list"))
