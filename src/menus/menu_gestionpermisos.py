from complementos.complementos import limpiar_pantalla
from getpass import getpass
from persistencia.usuario_dao import UsuarioDAO


def menu_dominio_gestionPermisos(dao_usuario: UsuarioDAO, gestion_permisos):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO GESTION PERMISOS (DEMOSTRACION) =====")
        print("1. Ver usuarios y permisos")
        print("2. Otorgar permiso")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            for u in dao_usuario.obtener_todos():
                print(f"ID: {u._id_usuario} | {u._nombre_usuario} "
                      f"| Permisos: {', '.join(u._permisos) or 'Sin permisos'}")

        elif opcion == "2":
            try:
                id_enc = int(input("ID encargado: "))
                enc = dao_usuario.obtener_por_id(id_enc)
                if enc is None:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                clave = getpass("Contraseña del encargado: ")
                if not enc.autenticar(clave):
                    print("Contraseña incorrecta.")
                    input("\nPresione Enter...")
                    continue
                id_dest = int(input("ID destinatario: "))
                dest = dao_usuario.obtener_por_id(id_dest)
                if dest is None:
                    print("No encontrado.")
                    input("\nPresione Enter...")
                    continue
                permiso = input("Permiso: ").strip()
                if gestion_permisos.otorgar_permiso(enc, dest, permiso):
                    dao_usuario.actualizar(dest)
                    print("Permiso otorgado y guardado.")
                else:
                    print("No se pudo otorgar.")
            except ValueError:
                print("ID inválido.")

        else:
            print("Opción inválida.")
        input("\nPresione Enter...")