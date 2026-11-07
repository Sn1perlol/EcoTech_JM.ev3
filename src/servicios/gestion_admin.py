from servicios.api import obtener_datos, mostrar_indicador, DATOS_RESPALDO
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from dominio.usuario import Usuario


class ServicioGestionAdmin:

    def __init__(self, db_path: str = "ecotech.db"):
        self.usuario_dao = UsuarioDAO(db_path)

    def _exigir_admin(self, usuario_sesion: Usuario):
        if usuario_sesion is None:
            raise PermissionError("Acceso denegado: No hay una sesión activa.")
        if "administrar_permisos" not in usuario_sesion.permisos:
            raise PermissionError("Acceso denegado: Se requieren permisos de administrador.")

    def listar_cuentas(self, usuario_sesion: Usuario):
        self._exigir_admin(usuario_sesion)
        return self.usuario_dao.obtener_todos()

    def crear_usuario_admin(self, usuario_sesion, username, mail, clave, id_empleado):
        self._exigir_admin(usuario_sesion)
        if self.usuario_dao.obtener_por_nombre(username) is not None:
            raise ValueError("El nombre de usuario ya está registrado.")
        if EmpleadoDAO.buscar_por_id(id_empleado) is None:
            raise ValueError("El empleado asociado no existe.")
        nuevo = Usuario(nombre_usuario=username, mail=mail, contrasenia=clave, id_empleado=id_empleado)
        nuevo.agregar_permiso("administrar_permisos", usuario_sesion)
        if not self.usuario_dao.crear(nuevo):
            raise ValueError("No se pudo registrar el usuario en la base de datos.")
        return nuevo

    def otorgar_permiso(self, usuario_sesion, id_usuario_destino, permiso):
        self._exigir_admin(usuario_sesion)
        destino = self.usuario_dao.obtener_por_id(id_usuario_destino)
        if destino is None:
            raise ValueError("El usuario destinatario no existe.")
        if not destino.agregar_permiso(permiso, usuario_sesion):
            raise ValueError("No se pudo otorgar el permiso. Permiso vacío o ya asignado.")
        self.usuario_dao.actualizar(destino)
        return True

    def eliminar_usuario(self, usuario_sesion, id_usuario_eliminar):
        self._exigir_admin(usuario_sesion)
        if usuario_sesion.id_usuario == id_usuario_eliminar:
            raise ValueError("No puedes eliminar tu propio usuario en sesión.")
        return self.usuario_dao.eliminar(id_usuario_eliminar)

    def listar_empleados(self, usuario_sesion):
        self._exigir_admin(usuario_sesion)
        return EmpleadoDAO.listar()

    def consultar_indicador_dolar(self, usuario_sesion):
        self._exigir_admin(usuario_sesion)
        try:
            datos, origen = obtener_datos()
            mostrar_indicador(datos, origen)
        except Exception:
            print("\n[AVISO] Cargando datos locales de respaldo...\n")
            mostrar_indicador(DATOS_RESPALDO, "datos de respaldo (local)")