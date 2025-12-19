import secrets
import string

def generate_qr_code() -> str:
    """
    Genera código QR único para cooperativista
    Formato: COOP-XXXXXXXXXXXX (12 caracteres alfanuméricos)
    """
    chars = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(chars) for _ in range(12))
    return f"COOP-{code}"


def generate_short_qr() -> str:
    """
    Genera código QR corto (8 caracteres)
    Formato: COOP-XXXXXXXX
    """
    chars = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(chars) for _ in range(8))
    return f"COOP-{code}"
