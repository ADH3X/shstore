# init_db.py
from shstore import create_app, db
from shstore.models import User, Category, Product
from shstore.utils.security import hash_password

app = create_app()

with app.app_context():
    # ---- Crear todas las tablas ----
    db.create_all()
    print("✔ Tablas creadas correctamente.")

    # ---- Usuario admin por defecto ----
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password=hash_password("1234"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("✔ Usuario admin creado (user: admin / pass: 1234)")
    else:
        print("ℹ Usuario admin ya existía, no se creó otro.")

    # ---- Categorías base ----
    default_categories = [
        ("todo", "Todo"),
        ("hombre", "Hombre"),
        ("mujer", "Mujer"),
        ("calzado", "Calzado"),
        ("accesorios", "Accesorios"),
        ("outlet", "Outlet"),
    ]

    for slug, name in default_categories:
        cat = Category.query.filter_by(slug=slug).first()
        if not cat:
            cat = Category(slug=slug, name=name)
            db.session.add(cat)

    db.session.commit()
    print("✔ Categorías base creadas/actualizadas.")

    # ---- Producto demo ----
    if not Product.query.first():
        cat_hombre = Category.query.filter_by(slug="hombre").first()

        demo = Product(
            name="Campera negra básica",
            slug="campera-negra-basica",
            price=180,
            description="Campera negra básica unisex de uso diario.",
            # IMPORTANTE: usamos la relación Category, no un string
            category=cat_hombre,
        )

        db.session.add(demo)
        db.session.commit()
        print("✔ Producto de prueba insertado.")
    else:
        print("ℹ Ya había productos, no se insertó demo.")

