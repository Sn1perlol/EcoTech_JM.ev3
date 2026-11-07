from getpass import getpass
from complementos.complementos import limpiar_pantalla
from servicios.gestion_admin import ServicioGestionAdmin


def menu_gestion_admin(usuario_sesion):
    servicio = ServicioGestionAdmin("ecotech.db")
    while True:
        limpiar_pantalla()
        print("\n===== MÓDULO DE GESTIÓN ADMINISTRATIVA =====")
        print("1. Listar cuentas")
        print("2. Registrar nuevo admin")
        print("3. Otorgar permiso")
        print("4. Eliminar cuenta")
        print("5. Listar empleados")
        print("6. Consultar Dólar (API)")
        print("0. Volver")

        opcion = input("\nOpción: ").strip()
        limpiar_pantalla()
        if opcion == "0":
            return
        try:
            if opcion == "1":
                for u in servicio.listar_cuentas(usuario_sesion):
                    permisos = ", ".join(u.permisos) or "Sin permisos"
                    print(f"ID: {u.id_usuario} | {u.nombre_usuario} | Emp: {u._empleado} | {permisos}")
            elif opcion == "2":
                username = input("Usuario: ").strip()
                mail = input("Correo: ").strip()
                clave = getpass("Contraseña: ")
                id_emp = int(input("ID empleado: "))
                nuevo = servicio.crear_usuario_admin(usuario_sesion, username, mail, clave, id_emp)
                print(f"Creado: {nuevo.nombre_usuario} (ID {nuevo.id_usuario})")
            elif opcion == "3":
                id_dest = int(input("ID destinatario: "))
                permiso = input("Permiso: ").strip()
                servicio.otorgar_permiso(usuario_sesion, id_dest, permiso)
                print("Otorgado y guardado.")
            elif opcion == "4":
                id_elim = int(input("ID a eliminar: "))
                if input(f"¿Eliminar {id_elim}? (s/n): ").lower() == "s":
                    print("Eliminado." if servicio.eliminar_usuario(usuario_sesion, id_elim) else "No encontrado.")
            elif opcion == "5":
                for emp in servicio.listar_empleados(usuario_sesion):
                    print(emp.mostrar_datos())
            elif opcion == "6":
                servicio.consultar_indicador_dolar(usuario_sesion)
            else:
                print("Opción inválida.")
        except PermissionError as err:
            print(f"Permisos: {err}")
        except ValueError as err:
            print(f"Datos: {err}")
        except Exception as err:
            print(f"Error: {err}")
        input("\nPresione Enter...")