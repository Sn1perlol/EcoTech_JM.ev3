from datetime import datetime
from dominio.registrotiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.registrotiempo_dao import RegistroTiempoDAO
from menus.menuregistrotiempo import main_RegistroTiempo
from complementos.complementos import (
    limpiar_pantalla, validar_entero_positivo, validar_fecha_DD_MM_YYYY,
    validar_texto_longitud,
)
from entradas import pedir_dato


def _parse_fecha(ddmmyyyy):
    return datetime.strptime(ddmmyyyy, "%d-%m-%Y").date()


def menu_dominio_registro_tiempo():
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO REGISTRO DE TIEMPO =====")
        print("1. Registrar horas de trabajo")
        print("2. Listar todos los registros")
        print("3. Ver registros de un empleado")
        print("4. Ver registros de un proyecto")
        print("5. Gestionar registros de tiempo (CRUD)")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return
        if opcion == "5":
            main_RegistroTiempo()
            continue

        if opcion == "1":
            try:
                id_e = pedir_dato("ID empleado: ", lambda v: validar_entero_positivo(v, "ID"))
                emp = EmpleadoDAO.buscar_por_id(id_e)
                if emp is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter...")
                    continue
                id_p = pedir_dato("ID proyecto: ", lambda v: validar_entero_positivo(v, "ID"))
                proy = ProyectoDao.buscar_por_id(id_p)
                if proy is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter...")
                    continue
                if not RegistroTiempoDAO.empleado_asignado(emp._id, proy._id_proyecto):
                    print("El empleado no está asignado a ese proyecto.")
                    input("\nPresione Enter...")
                    continue
                horas = pedir_dato("Horas: ", lambda v: validar_entero_positivo(v, "Horas"))
                fecha_str = pedir_dato("Fecha (DD-MM-YYYY): ", validar_fecha_DD_MM_YYYY)
                fecha = _parse_fecha(fecha_str)
                desc = pedir_dato("Descripción (máx 200): ",
                                  lambda v: validar_texto_longitud(v, 200, "Descripción"))
                reg = RegistroTiempo(emp, proy, fecha, horas, desc)
                if RegistroTiempoDAO.insertar(reg):
                    print("Registro guardado con ID:", reg._id_registro)
                else:
                    print("No se pudo guardar.")
            except Exception as error:
                print("Error:", error)

        elif opcion == "2":
            for r in RegistroTiempoDAO.listar():
                print(f"ID: {r._id_registro} | Empleado: {r._empleado._nombre} "
                      f"| Proyecto: {r._proyecto._nombre} | Fecha: {r._fecha_trabajada} "
                      f"| Horas: {r._horas_trabajadas} | {r._descripcion_tarea}")

        elif opcion == "3":
            try:
                id_e = pedir_dato("ID empleado: ", lambda v: validar_entero_positivo(v, "ID"))
                emp = EmpleadoDAO.buscar_por_id(id_e)
                if emp is None:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                propios = [r for r in RegistroTiempoDAO.listar() if r._empleado._id == emp._id]
                if not propios:
                    print("Sin registros.")
                else:
                    for r in propios:
                        print(f"ID: {r._id_registro} | {r._proyecto._nombre} "
                              f"| {r._fecha_trabajada} | {r._horas_trabajadas} h")
                    print("Total:", sum(r._horas_trabajadas for r in propios), "h")
            except Exception as error:
                print("Error:", error)

        elif opcion == "4":
            try:
                id_p = pedir_dato("ID proyecto: ", lambda v: validar_entero_positivo(v, "ID"))
                proy = ProyectoDao.buscar_por_id(id_p)
                if proy is None:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                propios = [r for r in RegistroTiempoDAO.listar()
                           if r._proyecto._id_proyecto == proy._id_proyecto]
                if not propios:
                    print("Sin registros.")
                else:
                    for r in propios:
                        print(f"ID: {r._id_registro} | {r._empleado._nombre} "
                              f"| {r._fecha_trabajada} | {r._horas_trabajadas} h")
                    print("Total:", sum(r._horas_trabajadas for r in propios), "h")
            except Exception as error:
                print("Error:", error)

        else:
            print("Opción inválida.")
        input("\nPresione Enter...")