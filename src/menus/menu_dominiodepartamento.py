from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from menus.menudepartamento import main_departamento
from complementos.complementos import limpiar_pantalla


def menu_dominio_departamento():
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO DEPARTAMENTO =====")
        print("1. Contratar empleado (autorizado por RRHH)")
        print("2. Agregar empleado al departamento")
        print("3. Quitar empleado del departamento")
        print("4. Vincular proyecto existente al departamento")
        print("5. Editar nombre de un proyecto del departamento")
        print("6. Desvincular proyecto del departamento")
        print("7. Gestionar departamentos (CRUD)")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()
        if opcion == "0":
            return
        if opcion == "7":
            main_departamento()
            continue
        if opcion not in ("1", "2", "3", "4", "5", "6"):
            print("Opcion no valida.")
            input("\nPresione Enter...")
            continue

        try:
            id_dep = int(input("ID del departamento: "))
            depto = DepartamentoDAO.buscar_por_id(id_dep)
            if depto is None:
                print("Departamento no encontrado.")
                input("\nPresione Enter...")
                continue

            if opcion in ("1", "2", "3"):
                id_emp = int(input("ID del empleado: "))
                emp = EmpleadoDAO.buscar_por_id(id_emp)
                if emp is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter...")
                    continue
                asociado = next((e for e in depto._empleados if e._id == emp._id), None)

                if opcion == "1":
                    if asociado:
                        print("Ya pertenece al departamento.")
                    else:
                        id_enc = int(input("ID del encargado de RRHH: "))
                        enc = EmpleadoDAO.buscar_por_id(id_enc)
                        if enc and depto.contratar_empleado(emp, enc):
                            if DepartamentoDAO.agregar_empleado(depto, emp):
                                print("Contratado y guardado.")
                            else:
                                print("No se pudo guardar.")
                        else:
                            print("No autorizado (encargado debe ser RRHH).")

                elif opcion == "2":
                    if asociado:
                        print("Ya pertenece.")
                    elif depto.agregar_empleado(emp):
                        if DepartamentoDAO.agregar_empleado(depto, emp):
                            print("Agregado y guardado.")
                        else:
                            print("No se pudo guardar.")

                elif opcion == "3":
                    if not asociado:
                        print("No pertenece.")
                    else:
                        depto.eliminar_empleado(asociado)
                        if DepartamentoDAO.quitar_empleado(depto, emp):
                            print("Desvinculado.")
                        else:
                            print("No se pudo quitar.")

            elif opcion in ("4", "5", "6"):
                id_p = int(input("ID del proyecto: "))
                proy = ProyectoDao.buscar_por_id(id_p)
                if proy is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter...")
                    continue
                asociado = next((p for p in depto._proyectos if p._id_proyecto == proy._id_proyecto), None)

                if opcion == "4":
                    if asociado:
                        print("Ya pertenece.")
                    elif depto.crear_proyecto(proy):
                        if DepartamentoDAO.agregar_proyecto(depto, proy):
                            print("Vinculado.")
                        else:
                            print("No se pudo guardar.")

                elif opcion == "5":
                    if not asociado:
                        print("No pertenece.")
                        input("\nPresione Enter...")
                        continue
                    nuevo = input("Nuevo nombre: ").strip()
                    if depto.editar_proyecto(asociado, nuevo):
                        if ProyectoDao.actualizar(asociado):
                            print("Actualizado.")

                elif opcion == "6":
                    if not asociado:
                        print("No pertenece.")
                    elif depto.eliminar_proyecto(asociado):
                        if DepartamentoDAO.quitar_proyecto(depto, asociado):
                            print("Desvinculado.")

        except ValueError as error:
            print("Datos incorrectos:", error)
        except Exception as error:
            print("Ocurrió un error:", error)
        input("\nPresione Enter...")