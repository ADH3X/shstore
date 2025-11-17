# shstore/utils/whatsapp.py

# Números oficiales
WHATSAPP_CONTACT_1 = "+59176333189"   # negocio
WHATSAPP_CONTACT_2 = "+59169259870"   # tu número Adhex CORREGIDO

def format_whatsapp_message(product_name: str, price: float) -> str:
    """
    Genera el mensaje para enviar por WhatsApp
    """
    return f"Quiero comprar: {product_name} ({price} Bs)"


def whatsapp_link(number: str, message: str) -> str:
    """
    Devuelve el link de WhatsApp correctamente formateado.
    """
    clean = number.replace("+", "").replace(" ", "")
    encoded = message.replace(" ", "%20")  # si quieres mejorar esto luego usamos quote_plus
    return f"https://wa.me/{clean}?text={encoded}"
