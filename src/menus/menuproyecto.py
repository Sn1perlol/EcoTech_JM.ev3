from persistencia.proyecto_dao import ProyectoDAO
from dominio.proyecto import Proyecto
from datetime import date


def _pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingrese un número válido.")


def _crear_proyecto():
    print("\n--- Crear Proyecto ---")
    nombre = input("Nombre del proyecto: ").strip()
    fecha_str = input("Fecha de inicio (YYYY-MM-DD): ").strip()
    descripcion = input("Descripción: ").strip()

    try:
        fecha = date.fromisoformat(fecha_str)
    except ValueError:
        print("Formato de fecha inválido. Use YYYY-MM-DD.")
        return

    proyecto = Proyecto(
        id_proyecto=None,
        nombre=nombre,
        fecha_inicio=fecha,
        descripcion=descripcion
    )
    ProyectoDAO.insertar(proyecto)
    print(f"Proyecto creado con ID {proyecto._idProyecto}.")


def _listar_proyectos():
    print("\n--- Lista de Proyectos ---")
    proyectos = ProyectoDAO.listar()
    if not proyectos:
        print("No hay proyectos registrados.")
        return
    for p in proyectos:
        print(f"  {p}")


def _buscar_proyecto():
    print("\n--- Buscar Proyecto ---")
    print("1. Por ID")
    print("2. Por nombre")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        id_proy = _pedir_entero("ID del proyecto: ")
        p = ProyectoDAO.buscar_por_id(id_proy)
        if p is None:
            print("Proyecto no encontrado.")
        else:
            print(f"  {p}")
    elif opcion == "2":
        nombre = input("Nombre (o parte): ").strip()
        resultados = ProyectoDAO.buscar_por_nombre(nombre)
        if not resultados:
            print("Sin coincidencias.")
        else:
            for p in resultados:
                print(f"  {p}")
    else:
        print("Opción inválida.")


def _actualizar_proyecto():
    print("\n--- Actualizar Proyecto ---")
    id_proy = _pedir_entero("ID del proyecto a actualizar: ")
    p = ProyectoDAO.buscar_por_id(id_proy)
    if p is None:
        print("Proyecto no encontrado.")
        return

    nuevo_nombre = input(f"Nuevo nombre [{p._nombre}]: ").strip()
    nueva_desc = input(f"Nueva descripción [{p._descripcion}]: ").strip()

    if nuevo_nombre:
        p._nombre = nuevo_nombre
    if nueva_desc:
        p._descripcion = nueva_desc

    if ProyectoDAO.actualizar(p):
        print("Proyecto actualizado.")
    else:
        print("No se pudo actualizar.")


def _eliminar_proyecto():
    print("\n--- Eliminar Proyecto ---")
    id_proy = _pedir_entero("ID del proyecto a eliminar: ")
    confirmacion = input(f"¿Confirma eliminar el proyecto {id_proy}? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Operación cancelada.")
        return

    if ProyectoDAO.eliminar(id_proy):
        print("Proyecto eliminado.")
    else:
        print("Proyecto no encontrado.")


def _asignar_empleado():
    print("\n--- Asignar Empleado a Proyecto ---")
    id_proy = _pedir_entero("ID del proyecto: ")
    id_emp = _pedir_entero("ID del empleado: ")

    if ProyectoDAO.asignar_empleado(id_proy, id_emp):
        print("Empleado asignado correctamente.")
    else:
        print("No se pudo asignar.")


def _desvincular_empleado():
    print("\n--- Desvincular Empleado de Proyecto ---")
    id_proy = _pedir_entero("ID del proyecto: ")
    id_emp = _pedir_entero("ID del empleado: ")

    if ProyectoDAO.desvincular_empleado(id_proy, id_emp):
        print("Empleado desvinculado.")
    else:
        print("No se encontró la asignación.")


def _listar_empleados_proyecto():
    print("\n--- Empleados del Proyecto ---")
    id_proy = _pedir_entero("ID del proyecto: ")
    ids = ProyectoDAO.listar_empleados(id_proy)
    if not ids:
        print("El proyecto no tiene empleados asignados.")
    else:
        print(f"  IDs de empleados: {ids}")


def menu_proyecto():
    while True:
        print("\n=== MENÚ PROYECTO ===")
        print("1. Crear proyecto")
        print("2. Listar proyectos")
        print("3. Buscar proyecto")
        print("4. Actualizar proyecto")
        print("5. Eliminar proyecto")
        print("6. Asignar empleado a proyecto")
        print("7. Desvincular empleado de proyecto")
        print("8. Listar empleados de un proyecto")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            _crear_proyecto()
        elif opcion == "2":
            _listar_proyectos()
        elif opcion == "3":
            _buscar_proyecto()
        elif opcion == "4":
            _actualizar_proyecto()
        elif opcion == "5":
            _eliminar_proyecto()
        elif opcion == "6":
            _asignar_empleado()
        elif opcion == "7":
            _desvincular_empleado()
        elif opcion == "8":
            _listar_empleados_proyecto()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")