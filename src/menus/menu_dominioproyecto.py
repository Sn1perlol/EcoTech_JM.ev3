from datetime import datetime
from complementos.complementos import (
    limpiar_pantalla, validar_entero_positivo, validar_fecha_DD_MM_YYYY,
    validar_texto_longitud,
)
from dominio.proyecto import Proyecto
from entradas import pedir_dato
from persistencia.proyecto_dao import ProyectoDao
from persistencia.empleado_dao import EmpleadoDAO


def _parse_fecha(ddmmyyyy):
    return datetime.strptime(ddmmyyyy, "%d-%m-%Y").date()


def mostrar_menu_proyecto():
    print("\n===== PROYECTOS - ECOTECH =====")
    print("1. Registrar Proyecto")
    print("2. Listar Proyectos")
    print("3. Buscar Proyecto")
    print("4. Actualizar Proyecto")
    print("5. Eliminar Proyecto")
    print("6. Asignar empleado a proyecto")
    print("7. Desvincular empleado de proyecto")
    print("0. Volver al menu principal")


def main_proyecto():
    while True:
        limpiar_pantalla()
        mostrar_menu_proyecto()
        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = pedir_dato("Nombre (máx 60): ",
                                    lambda v: validar_texto_longitud(v, 60, "Nombre"))
                fecha_str = pedir_dato("Fecha inicio (DD-MM-YYYY): ", validar_fecha_DD_MM_YYYY)
                fecha_inicio = _parse_fecha(fecha_str)
                desc = pedir_dato("Descripción (máx 200): ",
                                  lambda v: validar_texto_longitud(v, 200, "Descripción"))
                proy = Proyecto(nombre, desc, fecha_inicio)
                ProyectoDao.insertar(proy)
                print(f"\nProyecto registrado con ID: {proy._id_proyecto}")
            except Exception as error:
                print("\nError:", error)
            input("\nPresione Enter...")

        elif opcion == "2":
            for p in ProyectoDao.listar():
                print(f"ID: {p._id_proyecto} | {p._nombre} | {p._estado} | {p._fecha_inicio} | {p._descripcion}")
            input("\nPresione Enter...")

        elif opcion == "3":
            try:
                id_p = pedir_dato("ID: ", lambda v: validar_entero_positivo(v, "ID"))
                p = ProyectoDao.buscar_por_id(id_p)
                if p is None:
                    print("No encontrado.")
                else:
                    print(f"ID: {p._id_proyecto} | {p._nombre} | {p._estado}")
                    print(f"Inicio: {p._fecha_inicio} | Fin: {p._fecha_fin}")
                    print(f"Descripción: {p._descripcion}")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "4":
            try:
                id_p = pedir_dato("ID: ", lambda v: validar_entero_positivo(v, "ID"))
                p = ProyectoDao.buscar_por_id(id_p)
                if p is None:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                nom = input(f"Nombre [{p._nombre}]: ").strip()
                if nom:
                    p.actualizar_datos(nombre=nom)
                desc = input(f"Descripción [{p._descripcion}]: ").strip()
                if desc:
                    p.actualizar_datos(descripcion=desc)
                fec = input(f"Fecha inicio [{p._fecha_inicio}] (DD-MM-YYYY): ").strip()
                if fec:
                    p.actualizar_fechas(fecha_inicio=_parse_fecha(validar_fecha_DD_MM_YYYY(fec)))
                fin = input(f"Fecha fin [{p._fecha_fin}] (DD-MM-YYYY): ").strip()
                if fin:
                    p.actualizar_fechas(fecha_fin=_parse_fecha(validar_fecha_DD_MM_YYYY(fin)))
                est = input(f"Estado [{p._estado}]: ").strip()
                if est:
                    p.cambiar_estado(est)
                if ProyectoDao.actualizar(p):
                    print("Actualizado.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "5":
            try:
                id_p = pedir_dato("ID: ", lambda v: validar_entero_positivo(v, "ID"))
                p = ProyectoDao.buscar_por_id(id_p)
                if p and input(f"¿Eliminar {p._nombre}? (s/n): ").lower() == "s":
                    print("Eliminado." if ProyectoDao.eliminar(id_p) else "No se pudo eliminar.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "6":
            try:
                id_p = int(input("ID proyecto: "))
                p = ProyectoDao.buscar_por_id(id_p)
                id_e = int(input("ID empleado: "))
                e = EmpleadoDAO.buscar_por_id(id_e)
                if p and e and ProyectoDao.asignar_empleado(p, e):
                    print("Asignado.")
                else:
                    print("No se pudo asignar.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "7":
            try:
                id_p = int(input("ID proyecto: "))
                p = ProyectoDao.buscar_por_id(id_p)
                id_e = int(input("ID empleado: "))
                e = EmpleadoDAO.buscar_por_id(id_e)
                if p and e and ProyectoDao.desvincular_empleado(p, e):
                    print("Desvinculado.")
                else:
                    print("No se pudo desvincular.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "0":
            return
        else:
            print("Opción inválida.")
            input("\nPresione Enter...")