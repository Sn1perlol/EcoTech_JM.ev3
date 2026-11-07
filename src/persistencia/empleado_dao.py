from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.empleado import Empleado


def _a_iso(valor):
    """Convierte date/datetime a string ISO; deja strings/None como están."""
    if valor is None:
        return None
    if hasattr(valor, "isoformat"):
        return valor.isoformat()
    return valor


class EmpleadoDAO:

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id=fila[0], nombre=fila[1], direccion=fila[2], numero=fila[3],
            correo=fila[4], fecha_contrato=fila[5], salario=fila[6], cargo=fila[7]
        )

    @staticmethod
    def insertar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            fecha_iso = _a_iso(empleado._fecha_contrato)
            if empleado._id is not None:
                sql = ("INSERT INTO empleado "
                       "(id, nombre, direccion, numero, correo, fecha_contrato, salario, cargo) "
                       f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca}, {marca}, {marca}, {marca})")
                cursor.execute(sql, (empleado._id, empleado._nombre, empleado._direccion,
                                     empleado._numero, empleado._correo, fecha_iso,
                                     empleado._salario, empleado._cargo))
            else:
                sql = ("INSERT INTO empleado "
                       "(nombre, direccion, numero, correo, fecha_contrato, salario, cargo) "
                       f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca}, {marca}, {marca})")
                cursor.execute(sql, (empleado._nombre, empleado._direccion,
                                     empleado._numero, empleado._correo, fecha_iso,
                                     empleado._salario, empleado._cargo))
                empleado._id = cursor.lastrowid
            conexion.commit()
            if empleado._id is None:
                empleado._id = cursor.lastrowid
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = ("UPDATE empleado SET "
                   f"nombre = {marca}, direccion = {marca}, numero = {marca}, "
                   f"correo = {marca}, fecha_contrato = {marca}, "
                   f"salario = {marca}, cargo = {marca} WHERE id = {marca}")
            cursor.execute(sql, (empleado._nombre, empleado._direccion, empleado._numero,
                                 empleado._correo, _a_iso(empleado._fecha_contrato),
                                 empleado._salario, empleado._cargo, empleado._id))
            actualizado = cursor.rowcount > 0
            conexion.commit()
            return actualizado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"DELETE FROM empleado WHERE id = {marca}", (id_empleado,))
            eliminado = cursor.rowcount > 0
            conexion.commit()
            return eliminado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = ("SELECT id, nombre, direccion, numero, correo, "
                   "fecha_contrato, salario, cargo "
                   f"FROM empleado WHERE id = {marca}")
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return EmpleadoDAO._fila_a_empleado(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre, direccion, numero, correo, "
                "fecha_contrato, salario, cargo FROM empleado"
            )
            return [EmpleadoDAO._fila_a_empleado(f) for f in cursor.fetchall()]
        finally:
            if conexion:
                conexion.close()