import hashlib
import hmac
import secrets


class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 6

    def __init__(self, nombre_usuario, mail, contrasenia, id_empleado, id_usuario=None):
        if id_usuario is not None and (not isinstance(id_usuario, int) or id_usuario <= 0):
            raise ValueError("El ID del usuario debe ser un entero positivo.")
        if not isinstance(id_empleado, int) or id_empleado <= 0:
            raise ValueError("El ID del empleado debe ser un entero positivo.")

        self._id_usuario = id_usuario
        self._nombre_usuario = self.normalizar_usuario(nombre_usuario)
        self._mail = mail
        self._empleado = id_empleado
        self._permisos = []
        self._contrasenia_hash = self._crear_hash(contrasenia)

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def nombre_usuario(self):
        return self._nombre_usuario

    @property
    def permisos(self):
        return self._permisos.copy()

    def _crear_hash(self, contrasenia):
        sal = secrets.token_bytes(16)
        resultado = hashlib.pbkdf2_hmac("sha256", contrasenia.encode(), sal, 600000)
        return sal.hex() + ":" + resultado.hex()

    def autenticar(self, contrasenia):
        if not contrasenia:
            return False
        partes = self._contrasenia_hash.split(":")
        if len(partes) != 2:
            return False
        try:
            sal = bytes.fromhex(partes[0])
            hash_guardado = bytes.fromhex(partes[1])
        except ValueError:
            return False
        hash_ingresado = hashlib.pbkdf2_hmac("sha256", contrasenia.encode(), sal, 600000)
        return hmac.compare_digest(hash_ingresado, hash_guardado)

    def cambiar_contrasenia(self, contrasenia_actual, contrasenia_nueva):
        if not self.autenticar(contrasenia_actual):
            return False
        if not contrasenia_nueva or len(contrasenia_nueva) < self.MIN_CLAVE:
            return False
        if contrasenia_actual == contrasenia_nueva:
            return False
        self._contrasenia_hash = self._crear_hash(contrasenia_nueva)
        return True

    def agregar_permiso(self, permiso, encargado):
        if encargado is None:
            return False
        if "administrar_permisos" not in encargado._permisos:
            return False
        if not permiso or permiso.strip() == "":
            return False
        if permiso in self._permisos:
            return False
        self._permisos.append(permiso)
        return True

    @classmethod
    def normalizar_usuario(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError("Usuario fuera del largo permitido.")
        if not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
            raise ValueError("Use letras ASCII, números o guion bajo.")
        return nombre