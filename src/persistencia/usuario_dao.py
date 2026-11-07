import json
from typing import Optional, List

from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, marcador_sql


class UsuarioDAO:

    def __init__(self, db_path: str = None):
        # db_path se conserva por compatibilidad, pero la conexión real
        # se delega a conexion.abrir_conexion() (que respeta DB_ENGINE).
        self.db_path = db_path

    def _get_connection(self):
        return abrir_conexion()

    def crear(self, usuario: Usuario) -> Optional[int]:
        marca = marcador_sql()
        sql = (
            "INSERT INTO usuario (nombre_usuario, password_hash, id_empleado, permisos) "
            f"VALUES ({marca}, {marca}, {marca}, {marca})"
        )
        permisos_json = json.dumps(getattr(usuario, '_permisos', []))
        conexion = None
        try:
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute(sql, (usuario.nombre_usuario, usuario._contrasenia_hash,
                                 usuario._empleado, permisos_json))
            conexion.commit()
            usuario._id_usuario = cursor.lastrowid
            return usuario.id_usuario
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al registrar usuario (posible duplicado): {e}")
            return None
        finally:
            if conexion:
                conexion.close()

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        marca = marcador_sql()
        sql = (f"SELECT id, nombre_usuario, password_hash, id_empleado, permisos "
               f"FROM usuario WHERE id = {marca}")
        conexion = None
        try:
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute(sql, (id_usuario,))
            row = cursor.fetchone()
            if row:
                return self._mapear_a_objeto(row)
            return None
        finally:
            if conexion:
                conexion.close()

    def obtener_por_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        try:
            nombre_busqueda = Usuario.normalizar_usuario(nombre_usuario)
        except (TypeError, ValueError):
            return None
        marca = marcador_sql()
        sql = (f"SELECT id, nombre_usuario, password_hash, id_empleado, permisos "
               f"FROM usuario WHERE nombre_usuario = {marca}")
        conexion = None
        try:
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre_busqueda,))
            row = cursor.fetchone()
            if row:
                return self._mapear_a_objeto(row)
            return None
        finally:
            if conexion:
                conexion.close()

    def obtener_todos(self) -> List[Usuario]:
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado, permisos FROM usuario"
        usuarios = []
        conexion = None
        try:
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                usuarios.append(self._mapear_a_objeto(row))
        finally:
            if conexion:
                conexion.close()
        return usuarios

    def actualizar(self, usuario: Usuario) -> bool:
        if usuario.id_usuario is None:
            raise ValueError("El usuario debe estar registrado en la BD para actualizarse.")
        marca = marcador_sql()
        sql = (f"UPDATE usuario SET password_hash = {marca}, permisos = {marca} "
               f"WHERE id = {marca}")
        permisos_json = json.dumps(getattr(usuario, '_permisos', []))
        conexion = None
        try:
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute(sql, (usuario._contrasenia_hash, permisos_json, usuario.id_usuario))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            if conexion:
                conexion.close()

    def actualizar_contrasenia(self, usuario: Usuario) -> bool:
        return self.actualizar(usuario)

    def eliminar(self, id_usuario: int) -> bool:
        marca = marcador_sql()
        sql = f"DELETE FROM usuario WHERE id = {marca}"
        conexion = None
        try:
            conexion = self._get_connection()
            cursor = conexion.cursor()
            cursor.execute(sql, (id_usuario,))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            if conexion:
                conexion.close()

    def _mapear_a_objeto(self, row: tuple) -> Usuario:
        if len(row) == 5:
            id_db, nombre, hash_db, id_emp, permisos_raw = row
        else:
            id_db, nombre, hash_db, id_emp = row
            permisos_raw = None

        try:
            id_emp_int = int(id_emp)
            if id_emp_int <= 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError(f"Usuario '{nombre}' tiene id_empleado inválido: {id_emp!r}")

        usuario = Usuario.__new__(Usuario)
        usuario._id_usuario = id_db
        usuario._nombre_usuario = nombre
        usuario._mail = None
        usuario._empleado = id_emp_int
        usuario._contrasenia_hash = hash_db
        if permisos_raw:
            try:
                parsed = json.loads(permisos_raw)
                usuario._permisos = parsed if isinstance(parsed, list) else []
            except Exception:
                usuario._permisos = [permisos_raw]
        else:
            usuario._permisos = []
        return usuario