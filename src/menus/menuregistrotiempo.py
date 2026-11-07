from datetime import datetime
from complementos.complementos import limpiar_pantalla
from dominio.registrotiempo import RegistroTiempo
from persistencia.registrotiempo_dao import RegistroTiempoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao


def mostrar_menu_RegistroTiempo():
    print("\n===== REGISTROS DE TIEMPO =====")
    print("1. Registrar")
    print("2. Listar")
    print("3. Buscar")
    print("4. Actualizar")
    print("5. Eliminar")
    print("0. Volver")


def main_RegistroTiempo():
    while True:
        limpiar_pantalla()
        mostrar_menu_RegistroTiempo()
        opcion = input("Opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return
        try:
            if opcion == "1":
                emp = EmpleadoDAO.buscar_por_id(int(input("ID empleado: ")))
                proy = ProyectoDao.buscar_por_id(int(input("ID proyecto: ")))
                if not emp or not proy:
                    print("Empleado o proyecto no existe.")
                    input("\nPresione Enter...")
                    continue
                if not RegistroTiempoDAO.empleado_asignado(emp._id, proy._id_proyecto):
                    print("Empleado no asignado al proyecto.")
                    input("\nPresione Enter...")
                    continue
                horas = int(input("Horas: "))
                fecha = datetime.strptime(input("Fecha (DD-MM-YYYY): "), "%d-%m-%Y").date()
                desc = input("Descripción: ").strip()
                reg = RegistroTiempo(emp, proy, fecha, horas, desc)
                if RegistroTiempoDAO.insertar(reg):
                    print("Registro creado con ID:", reg._id_registro)

            elif opcion == "2":
                for r in RegistroTiempoDAO.listar():
                    print(f"ID: {r._id_registro} | Emp: {r._empleado._nombre} "
                          f"| Proy: {r._proyecto._nombre} | {r._fecha_trabajada} | {r._horas_trabajadas}h")

            elif opcion == "3":
                r = RegistroTiempoDAO.buscar_por_id(int(input("ID: ")))
                if r:
                    print(f"ID: {r._id_registro} | Emp: {r._empleado._nombre} "
                          f"| Proy: {r._proyecto._nombre} | {r._fecha_trabajada} | {r._horas_trabajadas}h")
                else:
                    print("No encontrado.")

            elif opcion == "4":
                r = RegistroTiempoDAO.buscar_por_id(int(input("ID: ")))
                if not r:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                h = input(f"Horas [{r._horas_trabajadas}]: ").strip()
                if h:
                    r._horas_trabajadas = int(h)
                f = input(f"Fecha [{r._fecha_trabajada}] (DD-MM-YYYY): ").strip()
                if f:
                    r._fecha_trabajada = datetime.strptime(f, "%d-%m-%Y").date()
                d = input(f"Descripción [{r._descripcion_tarea}]: ").strip()
                if d:
                    r._descripcion_tarea = d
                if RegistroTiempoDAO.actualizar(r):
                    print("Actualizado.")

            elif opcion == "5":
                id_r = int(input("ID a eliminar: "))
                if input("Confirmar (s/n): ").lower() == "s":
                    print("Eliminado." if RegistroTiempoDAO.eliminar(id_r) else "No se pudo eliminar.")
        except Exception as error:
            print("Error:", error)
        input("\nPresione Enter...")