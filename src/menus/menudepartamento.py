from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from complementos.complementos import limpiar_pantalla


def mostrar_menu_departementos():
    print("\n===== DEPARTAMENTOS - ECOTECH =====")
    print("1. Registrar Departamento")
    print("2. Listar Departamentos")
    print("3. Buscar Departamento")
    print("4. Actualizar Departamento")
    print("5. Eliminar Departamento")
    print("0. Volver al menu principal")


def main_departamento():
    while True:
        limpiar_pantalla()
        mostrar_menu_departementos()
        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = input("Nombre del departamento: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacio.")
                    input("\nPresione Enter...")
                    continue
                descripcion = input("Descripción: ").strip()
                gerente_texto = input("ID del gerente (Enter si no tiene): ").strip()
                gerente = None
                if gerente_texto:
                    gerente = EmpleadoDAO.buscar_por_id(int(gerente_texto))
                    if gerente is None:
                        print("El empleado indicado como gerente no existe.")
                        input("\nPresione Enter...")
                        continue
                departamento = Departamento(nombre, descripcion=descripcion, gerente=gerente)
                DepartamentoDAO.insertar(departamento)
                print("Departamento registrado con ID:", departamento._id_departamento)
            except ValueError:
                print("El ID del gerente debe ser numerico.")
            except Exception as error:
                print("Error al registrar el departamento:", error)

        elif opcion == "2":
            try:
                departamentos = DepartamentoDAO.listar()
                if not departamentos:
                    print("No hay departamentos registrados.")
                else:
                    for d in departamentos:
                        gerente_nombre = d._gerente._nombre if d._gerente else "Sin gerente"
                        print(f"ID: {d._id_departamento} | Nombre: {d._nombre} | Gerente: {gerente_nombre} | Desc: {d._descripcion}")
            except Exception as error:
                print("Error al listar departamentos:", error)

        elif opcion == "3":
            try:
                id_departamento = int(input("ID del departamento: "))
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    print("Departamento no encontrado.")
                else:
                    gerente_nombre = d._gerente._nombre if d._gerente else "Sin gerente"
                    print(f"ID: {d._id_departamento} | Nombre: {d._nombre} | Gerente: {gerente_nombre}")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al buscar departamento:", error)

        elif opcion == "4":
            try:
                id_departamento = int(input("ID del departamento a actualizar: "))
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    print("Departamento no encontrado.")
                    input("\nPresione Enter...")
                    continue
                nombre = input(f"Nombre [{d._nombre}]: ").strip()
                descripcion = input(f"Descripción [{d._descripcion}]: ").strip()
                gerente_texto = input(f"ID gerente [{d._gerente._id if d._gerente else 'Ninguno'}] (Enter para mantener): ").strip()
                
                if nombre:
                    d._nombre = nombre
                if descripcion:
                    d._descripcion = descripcion
                if gerente_texto:
                    gerente = EmpleadoDAO.buscar_por_id(int(gerente_texto))
                    if gerente is None:
                        print("El gerente indicado no existe.")
                        input("\nPresione Enter...")
                        continue
                    d._gerente = gerente
                
                if DepartamentoDAO.actualizar(d):
                    print("Departamento actualizado.")
                else:
                    print("No se detectaron cambios guardados.")
            except ValueError:
                print("El ID debe ser numerico.")
            except Exception as error:
                print("Error al actualizar departamento:", error)

        elif opcion == "5":
            try:
                id_departamento = int(input("ID del departamento a eliminar: "))
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    print("Departamento no encontrado.")
                    input("\nPresione Enter...")
                    continue
                confirmar = input(f"Eliminar {d._nombre}? (s/n): ").strip().lower()
                if confirmar == "s":
                    if DepartamentoDAO.eliminar(id_departamento):
                        print("Departamento eliminado.")
                    else:
                        print("No se pudo eliminar el departamento.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al eliminar departamento:", error)

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        input("\nPresione Enter...")