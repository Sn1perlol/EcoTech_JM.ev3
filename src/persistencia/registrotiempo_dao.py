from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.registrotiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao


def _a_iso(valor):
    if valor is None:
        return None
    if hasattr(valor, "isoformat"):
        return valor.isoformat()
    return valor


class RegistroTiempoDAO:

    @staticmethod
    def _asignacion_valida(cursor, marca, id_empleado, id_proyecto):
        cursor.execute(
            f"SELECT 1 FROM proyecto_empleado WHERE empleado_id = {marca} AND proyecto_id = {marca}",
            (id_empleado, id_proyecto))
        return cursor.fetchone() is not None

    @staticmethod
    def empleado_asignado(id_empleado, id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            return RegistroTiempoDAO._asignacion_valida(cursor, marca, id_empleado, id_proyecto)
        finally:
            conexion.close()

    @staticmethod
    def _fila_de_registroTiempo(fila):
        empleado = EmpleadoDAO.buscar_por_id(fila[4])
        proyecto = ProyectoDao.buscar_por_id(fila[5], cargar_relaciones=False)
        if empleado is None or proyecto is None:
            raise ValueError("El registro tiene un empleado o proyecto inexistente")
        # Firma real: (empleado, proyecto, fecha, horas, descripcion, id_registro)
        return RegistroTiempo(
            empleado, proyecto,
            fila[2],   # fecha_trabajada
            fila[1],   # horas_trabajadas
            fila[3],   # descripcion_tarea
            fila[0],   # id_registro
        )

    @staticmethod
    def insertar(registroTiempo):
        if registroTiempo._empleado is None or registroTiempo._proyecto is None:
            raise ValueError("El registro debe tener empleado y proyecto.")
        if registroTiempo._empleado._id is None or registroTiempo._proyecto._id_proyecto is None:
            raise ValueError("Empleado y proyecto deben estar guardados en la BD.")
        if registroTiempo._horas_trabajadas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            if not RegistroTiempoDAO._asignacion_valida(
                    cursor, marca, registroTiempo._empleado._id,
                    registroTiempo._proyecto._id_proyecto):
                raise ValueError("El empleado no está asignado a ese proyecto.")
            cursor.execute(
                "INSERT INTO registro_tiempo "
                "(horas_trabajadas, fecha_trabajada, descripcion_tarea, empleado_id, proyecto_id) "
                f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca})",
                (registroTiempo._horas_trabajadas,
                 _a_iso(registroTiempo._fecha_trabajada),
                 registroTiempo._descripcion_tarea,
                 registroTiempo._empleado._id,
                 registroTiempo._proyecto._id_proyecto))
            conexion.commit()
            registroTiempo._id_registro = cursor.lastrowid
            return registroTiempo
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def actualizar(registroTiempo):
        if registroTiempo._empleado is None or registroTiempo._proyecto is None:
            raise ValueError("El registro debe tener empleado y proyecto.")
        if registroTiempo._empleado._id is None or registroTiempo._proyecto._id_proyecto is None:
            raise ValueError("Empleado y proyecto deben estar guardados en la BD.")
        if registroTiempo._horas_trabajadas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            if not RegistroTiempoDAO._asignacion_valida(
                    cursor, marca, registroTiempo._empleado._id,
                    registroTiempo._proyecto._id_proyecto):
                raise ValueError("El empleado no está asignado a ese proyecto.")
            cursor.execute(
                "UPDATE registro_tiempo SET "
                f"horas_trabajadas = {marca}, fecha_trabajada = {marca}, "
                f"descripcion_tarea = {marca}, empleado_id = {marca}, "
                f"proyecto_id = {marca} WHERE id = {marca}",
                (registroTiempo._horas_trabajadas,
                 _a_iso(registroTiempo._fecha_trabajada),
                 registroTiempo._descripcion_tarea,
                 registroTiempo._empleado._id,
                 registroTiempo._proyecto._id_proyecto,
                 registroTiempo._id_registro))
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
    def eliminar(id_registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"DELETE FROM registro_tiempo WHERE id = {marca}", (id_registro,))
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
    def buscar_por_id(id_registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                "SELECT id, horas_trabajadas, fecha_trabajada, descripcion_tarea, "
                f"empleado_id, proyecto_id FROM registro_tiempo WHERE id = {marca}",
                (id_registro,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return RegistroTiempoDAO._fila_de_registroTiempo(fila)
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
                "SELECT id, horas_trabajadas, fecha_trabajada, descripcion_tarea, "
                "empleado_id, proyecto_id FROM registro_tiempo")
            return [RegistroTiempoDAO._fila_de_registroTiempo(f) for f in cursor.fetchall()]
        finally:
            if conexion:
                conexion.close()