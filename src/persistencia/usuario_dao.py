import sqlite3
import json
from typing import Optional, List
from dominio.usuario import Usuario


class UsuarioDAO:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def crear(self, usuario: Usuario) -> Optional[int]:
        sql = """
            INSERT INTO usuario (nombre_usuario, password_hash, id_empleado, permisos)
            VALUES (?, ?, ?, ?);
        """
        permisos_json = json.dumps(getattr(usuario, '_permisos', []))
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (usuario.nombre_usuario, usuario._contrasenia_hash,
                                     usuario._empleado, permisos_json))
                conn.commit()
                usuario._id_usuario = cursor.lastrowid
                return usuario.id_usuario
        except sqlite3.IntegrityError as e:
            print(f"Error al registrar usuario (posible duplicado): {e}")
            return None

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado, permisos FROM usuario WHERE id = ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_usuario,))
            row = cursor.fetchone()
            if row:
                return self._mapear_a_objeto(row)
        return None

    def obtener_por_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado, permisos FROM usuario WHERE nombre_usuario = ?;"
        try:
            nombre_busqueda = Usuario.normalizar_usuario(nombre_usuario)
        except (TypeError, ValueError):
            return None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (nombre_busqueda,))
            row = cursor.fetchone()
            if row:
                return self._mapear_a_objeto(row)
        return None

    def obtener_todos(self) -> List[Usuario]:
        sql = "SELECT id, nombre_usuario, password_hash, id_empleado, permisos FROM usuario;"
        usuarios = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                usuarios.append(self._mapear_a_objeto(row))
        return usuarios

    def actualizar(self, usuario: Usuario) -> bool:
        if usuario.id_usuario is None:
            raise ValueError("El usuario debe estar registrado en la BD para actualizarse.")
        sql = "UPDATE usuario SET password_hash = ?, permisos = ? WHERE id = ?;"
        permisos_json = json.dumps(getattr(usuario, '_permisos', []))
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (usuario._contrasenia_hash, permisos_json, usuario.id_usuario))
            conn.commit()
            return cursor.rowcount > 0

    def actualizar_contrasenia(self, usuario: Usuario) -> bool:
        return self.actualizar(usuario)

    def eliminar(self, id_usuario: int) -> bool:
        sql = "DELETE FROM usuario WHERE id = ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0

    def _mapear_a_objeto(self, row: tuple) -> Usuario:
        if len(row) == 5:
            id_db, nombre, hash_db, id_emp, permisos_raw = row
        else:
            id_db, nombre, hash_db, id_emp = row
            permisos_raw = None
        usuario = Usuario.__new__(Usuario)
        usuario._id_usuario = id_db
        usuario._nombre_usuario = nombre
        usuario._mail = None
        usuario._empleado = id_emp
        usuario._contrasenia_hash = hash_db
        if permisos_raw:
            try:
                usuario._permisos = json.loads(permisos_raw)
            except Exception:
                usuario._permisos = [permisos_raw]
        else:
            usuario._permisos = []
        return usuario