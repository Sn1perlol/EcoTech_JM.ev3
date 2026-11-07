from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO


def registrar_usuario(empleado_id, nombre_usuario, clave):
    nombre = Usuario.normalizar_usuario(nombre_usuario)
    dao = UsuarioDAO("ecotech.db")
    if dao.obtener_por_nombre(nombre) is not None:
        raise ValueError("Usuario duplicado.")
    usuario = Usuario(nombre, None, clave, empleado_id)
    return dao.crear(usuario)


def autenticar(nombre_usuario, contrasenia):
    dao = UsuarioDAO("ecotech.db")
    cuenta = dao.obtener_por_nombre(nombre_usuario)
    if cuenta is None or not cuenta.autenticar(contrasenia):
        return None
    return {
        "id": cuenta.id_usuario,
        "empleado_id": cuenta._empleado,
        "nombre_usuario": cuenta.nombre_usuario,
    }