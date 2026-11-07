from complementos.complementos import limpiar_pantalla


def menu_dominio_gestionDepartamento(gestion_departamentos):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO GESTION DEPARTAMENTO (DEMOSTRACION) =====")
        print("1. Crear departamento")
        print("2. Buscar departamento")
        print("3. Editar departamento")
        print("4. Eliminar departamento")
        print("5. Listar departamentos de la demostracion")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            nombre = input("Nombre: ").strip()
            d = gestion_departamentos.crear_departamento(nombre)
            if d is False:
                print("No se pudo crear.")
            else:
                print("Creado:", d._nombre)

        elif opcion == "2":
            nombre = input("Nombre a buscar: ").strip()
            d = gestion_departamentos.buscar_departamento(nombre)
            if d is False:
                print("No encontrado.")
            else:
                print("Encontrado:", d._nombre)

        elif opcion == "3":
            nombre = input("Nombre actual: ").strip()
            d = gestion_departamentos.buscar_departamento(nombre)
            if d is False:
                print("No encontrado.")
                input("\nPresione Enter...")
                continue
            nuevo = input("Nuevo nombre: ").strip()
            if gestion_departamentos.editar_departamento(d, nuevo):
                print("Actualizado:", d._nombre)
            else:
                print("No se pudo actualizar.")

        elif opcion == "4":
            nombre = input("Nombre a eliminar: ").strip()
            d = gestion_departamentos.buscar_departamento(nombre)
            if d is False:
                print("No encontrado.")
                input("\nPresione Enter...")
                continue
            if input("Confirmar (s/n): ").lower() != "s":
                print("Cancelado.")
            elif gestion_departamentos.eliminar_departamento(d):
                print("Eliminado.")
            else:
                print("No se puede eliminar (tiene empleados/proyectos).")

        elif opcion == "5":
            if not gestion_departamentos._departamentos:
                print("No hay departamentos en la demo.")
            else:
                for d in gestion_departamentos._departamentos:
                    print("-", d._nombre)

        else:
            print("Opción inválida.")
        input("\nPresione Enter...")