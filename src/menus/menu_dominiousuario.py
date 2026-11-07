from complementos.complementos import (
    limpiar_pantalla, validar_correo, validar_texto_longitud, validar_entero_positivo
)
from getpass import getpass
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from entradas import pedir_dato


def menu_dominio_usuario(dao_or_class):
    if isinstance(dao_or_class, type):
        usuario_dao = dao_or_class()
    else:
        usuario_dao = dao_or_class

    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO USUARIO =====")
        print("1. Crear usuario para un empleado")
        print("2. Autenticar usuario")
        print("3. Cambiar contraseña")
        print("4. Listar usuarios")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            print("Regresando al menú principal...")
            return

        elif opcion == "1":
            try:
                id_emp = pedir_dato("ID empleado: ", lambda v: validar_entero_positivo(v, "ID"))
                emp = EmpleadoDAO.buscar_por_id(id_emp)
                if emp is None:
                    print("\nEmpleado no encontrado.")
                    input("\nPresione Enter...")
                    continue
                nombre = pedir_dato("Usuario (máx 30): ",
                                    lambda v: validar_texto_longitud(v, 30, "Usuario"))
                mail = pedir_dato("Correo: ", lambda v: validar_correo(v, 80))
                clave = getpass(f"Contraseña (mín {Usuario.MIN_CLAVE}): ")
                if len(clave) < Usuario.MIN_CLAVE:
                    print("Contraseña demasiado corta.")
                    input("\nPresione Enter...")
                    continue
                nuevo = Usuario(nombre, mail, clave, emp._id)
                if len(usuario_dao.obtener_todos()) == 0:
                    nuevo._permisos.append("administrar_permisos")
                    print("Primer usuario: admin.")
                id_gen = usuario_dao.crear(nuevo)
                if id_gen:
                    print(f"\nUsuario guardado con ID: {id_gen}")
                else:
                    print("No se pudo crear.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "2":
            try:
                nombre = input("Usuario: ").strip()
                clave = getpass("Contraseña: ")
                u = usuario_dao.obtener_por_nombre(nombre)
                if u and u.autenticar(clave):
                    print(f"\n¡Bienvenido, {u.nombre_usuario}!")
                else:
                    print("\nCredenciales incorrectas.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "3":
            try:
                nombre = input("Usuario: ").strip()
                u = usuario_dao.obtener_por_nombre(nombre)
                if u:
                    actual = getpass("Contraseña actual: ")
                    nueva = getpass(f"Nueva contraseña (mín {Usuario.MIN_CLAVE}): ")
                    if u.cambiar_contrasenia(actual, nueva):
                        usuario_dao.actualizar(u)
                        print("\n¡Contraseña actualizada!")
                    else:
                        print("\nNo se pudo cambiar.")
                else:
                    print("Usuario no existe.")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")

        elif opcion == "4":
            for u in usuario_dao.obtener_todos():
                print(f"ID: {u.id_usuario} | {u.nombre_usuario} | Empleado: {u._empleado}")
            input("\nPresione Enter...")

        else:
            print("Opción inválida.")
            input("\nPresione Enter...")