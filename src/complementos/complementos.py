import os
import re


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def validar_texto_longitud(texto: str, max_longitud: int = 50, campo: str = "Texto") -> str:
    texto_limpio = texto.strip()
    if not texto_limpio:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    if len(texto_limpio) > max_longitud:
        raise ValueError(f"'{campo}' excede {max_longitud} caracteres.")
    return texto_limpio


def validar_nombre(nombre: str, max_longitud: int = 50) -> str:
    n = validar_texto_longitud(nombre, max_longitud=max_longitud, campo="Nombre")
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", n):
        raise ValueError("El nombre solo debe contener letras y espacios.")
    return n.title()


def validar_correo(correo: str, max_longitud: int = 100) -> str:
    c = validar_texto_longitud(correo, max_longitud=max_longitud, campo="Correo electrónico")
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", c):
        raise ValueError("Formato de correo inválido.")
    return c.lower()


def validar_telefono(telefono: str) -> str:
    t = telefono.strip()
    if not re.match(r"^\+?[0-9]{7,15}$", t):
        raise ValueError("Teléfono inválido (7–15 dígitos).")
    return t


def validar_entero_positivo(valor: str, campo: str = "Número") -> int:
    try:
        num = int(valor.strip())
        if num < 0:
            raise ValueError(f"'{campo}' no puede ser negativo.")
        return num
    except ValueError:
        raise ValueError(f"'{campo}' debe ser un entero válido.")


def validar_flotante_positivo(valor: str, campo: str = "Monto") -> float:
    try:
        num = float(valor.strip())
        if num < 0:
            raise ValueError(f"'{campo}' no puede ser negativo.")
        return num
    except ValueError:
        raise ValueError(f"'{campo}' debe ser un número válido.")


def validar_salario(salario_str: str, min_salario: float = 0.0,
                    max_salario: float = 5000000.0) -> float:
    s = validar_flotante_positivo(salario_str, campo="Salario")
    if s < min_salario or s > max_salario:
        raise ValueError(f"Salario fuera de rango (${min_salario:,.0f} – ${max_salario:,.0f}).")
    return s


def validar_fecha_DD_MM_YYYY(fecha_str: str) -> str:
    from datetime import datetime
    f = fecha_str.strip()
    try:
        datetime.strptime(f, "%d-%m-%Y")
        return f
    except ValueError:
        raise ValueError("La fecha debe tener formato DD-MM-YYYY.")