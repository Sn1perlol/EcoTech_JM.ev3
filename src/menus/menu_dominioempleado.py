from datetime import datetime
from complementos.complementos import (
    limpiar_pantalla, validar_correo, validar_entero_positivo,
    validar_fecha_DD_MM_YYYY, validar_nombre, validar_salario,
    validar_telefono, validar_texto_longitud,
)
from dominio.empleado import Empleado
from entradas import pedir_dato
from persistencia.empleado_dao import EmpleadoDAO


def mostrar_menu_empleado():
    print("\n===== EMPLEADOS - ECOTECH =====")
    print("1. Registrar Empleado")
    print("2. Listar Empleados")
    print("3. Buscar Empleado")
    print("4. Actualizar Empleado")
    print("5. Eliminar Empleado")
    print("0. Volver al menu principal")


def main_empleado():
    while True:
        limpiar_pantalla()
        mostrar_menu_empleado()
        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = pedir_dato("Nombre (máx 50): ", lambda v: validar_nombre(v, 50))
                direccion = pedir_dato("Dirección (máx 100): ",
                                       lambda v: validar_texto_longitud(v, 100, "Dirección"))
                numero = pedir_dato("Teléfono: ", validar_telefono)
                correo = pedir_dato("Correo (máx 80): ", lambda v: validar_correo(v, 80))
                fecha_str = pedir_dato("Fecha contrato (DD-MM-YYYY): ", validar_fecha_DD_MM_YYYY)
                fecha = datetime.strptime(fecha_str, "%d-%m-%Y").date()
                salario = pedir_dato("Salario: ", validar_salario)
                cargo = pedir_dato("Cargo (máx 40): ",
                                   lambda v: validar_texto_longitud(v, 40, "Cargo"))
                emp = Empleado(nombre, direccion, numero, correo, fecha, salario, cargo)
                EmpleadoDAO.insertar(emp)
                print(f"\nEmpleado registrado con ID: {emp._id}")
            except Exception as error:
                print("\nError al registrar:", error)
            input("\nPresione Enter...")

        elif opcion == "2":
            try:
                for emp in EmpleadoDAO.listar():
                    print(emp.mostrar_datos())
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "3":
            try:
                id_emp = pedir_dato("ID: ", lambda v: validar_entero_positivo(v, "ID"))
                emp = EmpleadoDAO.buscar_por_id(id_emp)
                if emp is None:
                    print("No encontrado.")
                else:
                    print(emp.mostrar_datos())
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "4":
            try:
                id_emp = pedir_dato("ID: ", lambda v: validar_entero_positivo(v, "ID"))
                emp = EmpleadoDAO.buscar_por_id(id_emp)
                if emp is None:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                nom = input(f"Nombre [{emp._nombre}]: ").strip()
                if nom:
                    emp._nombre = validar_nombre(nom, 50)
                EmpleadoDAO.actualizar(emp)
                print("Actualizado.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "5":
            try:
                id_emp = pedir_dato("ID: ", lambda v: validar_entero_positivo(v, "ID"))
                if input("Confirmar (s/n): ").lower() == "s":
                    if EmpleadoDAO.eliminar(id_emp):
                        print("Eliminado.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "0":
            return
        else:
            print("Opción inválida.")
            input("\nPresione Enter...")