# app/utils/security.py
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Inicializamos el hasher Argon2 con parámetros seguros por defecto
ph = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Devuelve el hash Argon2 del password en texto plano.
    """
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si el password en texto plano coincide con el hash almacenado.
    Retorna True o lanza una excepción en caso contrario.
    """
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
