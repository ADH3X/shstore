# shstore/models.py
from datetime import datetime
from . import db

# =====================================================
# CATEGORÍAS
# =====================================================
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    slug = db.Column(db.String(80), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Category {self.name}>"


# =====================================================
# PRODUCTO BASE
# =====================================================
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)

    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)

    # Categoría (relación con Category)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("Category", backref="products")

    # --------- INFO ESTRUCTURADA PARA FILTROS ----------
    # Marca (Nike, Adidas, Zara, etc.)
    brand = db.Column(db.String(100), nullable=True)

    # Color principal (negro, blanco, azul… -> se usará en un <select>)
    color = db.Column(db.String(50), nullable=True)

    # Género / público (Hombre, Mujer, Unisex, Niño, Niña…)
    gender = db.Column(db.String(20), nullable=True)

    # Estado (Nuevo, Como nuevo, Muy bueno, Bueno, Con detalles…)
    condition = db.Column(db.String(20), nullable=True)

    # Talla de ropa (XS, S, M, L, XL, 28, 30, 32…)
    size_clothes = db.Column(db.String(20), nullable=True)

    # Talla de calzado (34–45, etc.)
    size_shoes = db.Column(db.String(20), nullable=True)

    # Material principal (algodón, poliéster, cuero, denim…)
    material = db.Column(db.String(80), nullable=True)

    # Detalle de color (texto libre: “azul claro con detalles verde neón”)
    color_detail = db.Column(db.String(120), nullable=True)

    # Imagen principal de portada
    image_url = db.Column(db.String(300), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # GALERÍA COMPLETA (1 a 6 fotos)
    images = db.relationship(
        "ProductImage",
        back_populates="product",
        order_by="ProductImage.position",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# =====================================================
# VARIANTES (tallas sin stock por ahora)
# =====================================================
class ProductVariant(db.Model):
    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", backref="variants")

    size_system = db.Column(db.String(20), nullable=False)  # US, BR, LATAM, UNIQUE
    size_label = db.Column(db.String(20), nullable=False)   # 8, 9, 10 / S, M, L

    def __repr__(self):
        return f"<Variant {self.product_id} {self.size_system}-{self.size_label}>"


# =====================================================
# MÚLTIPLES IMÁGENES POR PRODUCTO
# =====================================================
class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="images")

    image_url = db.Column(db.String(300), nullable=False)

    is_main = db.Column(db.Boolean, default=False)

    # Para ordenar slider: 0 = la primera foto
    position = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<ProductImage {self.product_id} pos={self.position}>"


# =====================================================
# USUARIOS DEL SISTEMA
# =====================================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="admin")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"
