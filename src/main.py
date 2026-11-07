import os
import sys
from getpass import getpass

directorio_actual = os.path.dirname(os.path.abspath(__file__))
directorio_raiz = os.path.dirname(directorio_actual)

for ruta in [directorio_actual, directorio_raiz]:
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

from persistencia.crear_bd import crear_tablas
from persistencia.usuario_dao import UsuarioDAO
from persistencia.semilla import poblar_base_datos

from complementos.complementos import limpiar_pantalla
from dominio.gestion_departamentos import GestionDepartamento
from dominio.gestion_permisos import GestionPermisos

from menus.menu_dominiodepartamento import menu_dominio_departamento
from menus.menu_dominioempleado import main_empleado
from menus.menu_dominiogestiondepartamento import menu_dominio_gestionDepartamento
from menus.menu_gestionpermisos import menu_dominio_gestionPermisos
from menus.menu_dominioproyecto import main_proyecto
from menus.menu_dominioregistrotiempo import menu_dominio_registro_tiempo
from menus.menu_dominiousuario import menu_dominio_usuario
from menus.menu_gestionadmin import menu_gestion_admin
from menus.menu_api import menu_api


def _tiene_permiso(usuario, permiso):
    return permiso in getattr(usuario, "permisos", [])


def iniciar_sesion(usuario_dao: UsuarioDAO):
    intentos = 3
    while intentos > 0:
        limpiar_pantalla()
        print("===========================================")
        print("   INICIO DE SESIÓN - ECOTECH SOLUTIONS   ")
        print("===========================================\n")
        username = input("Nombre de usuario: ").strip()
        contrasenia = getpass("Contraseña: ").strip()
        usuario = usuario_dao.obtener_por_nombre(username)
        if usuario and usuario.autenticar(contrasenia):
            print(f"\n¡Autenticación exitosa! Bienvenido/a, {usuario.nombre_usuario}.")
            input("Presione Enter para ingresar al sistema...")
            return usuario
        intentos -= 1
        print(f"\nUsuario o contraseña incorrectos. Intentos restantes: {intentos}")
        input("Presione Enter para intentar nuevamente...")
    print("\nHas superado el número máximo de intentos. Cerrando la aplicación...")
    return None


def main():
    usuario_dao = UsuarioDAO("ecotech.db")
    gestion_permisos = GestionPermisos()
    gestion_departamentos = GestionDepartamento()

    usuario_logueado = iniciar_sesion(usuario_dao)
    if not usuario_logueado:
        return

    while True:
        limpiar_pantalla()
        print(f"\n===== ECOTECH SOLUTIONS | Sesión: {usuario_logueado.nombre_usuario} =====")
        print("1. Empleado")
        print("2. Departamento")
        print("3. Proyecto")
        print("4. Registro de Tiempo")
        print("5. Usuario (demostración)")
        print("6. Gestión de Permisos (demostración)")
        print("7. Gestión de Departamento (demostración)")
        if _tiene_permiso(usuario_logueado, "administrar_permisos"):
            print("8. Gestión Administración")
        print("9. Indicadores y Divisas (API)")
        print("0. Salir / Cerrar Sesión")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            if opcion == "1":
                limpiar_pantalla(); main_empleado()
            elif opcion == "2":
                limpiar_pantalla(); menu_dominio_departamento()
            elif opcion == "3":
                limpiar_pantalla(); main_proyecto()
            elif opcion == "4":
                limpiar_pantalla(); menu_dominio_registro_tiempo()
            elif opcion == "5":
                limpiar_pantalla(); menu_dominio_usuario(usuario_dao)
            elif opcion == "6":
                limpiar_pantalla(); menu_dominio_gestionPermisos(usuario_dao, gestion_permisos)
            elif opcion == "7":
                limpiar_pantalla(); menu_dominio_gestionDepartamento(gestion_departamentos)
            elif opcion == "8":
                if not _tiene_permiso(usuario_logueado, "administrar_permisos"):
                    print("\nAcceso denegado: se requieren permisos de administrador.")
                    input("Presione Enter para continuar...")
                    continue
                limpiar_pantalla(); menu_gestion_admin(usuario_logueado)
            elif opcion == "9":
                limpiar_pantalla(); menu_api()
            elif opcion == "0":
                limpiar_pantalla()
                print("Sesión cerrada. ¡Hasta luego!")
                break
            else:
                print("\nOpción no válida. Ingrese un número del 0 al 9.")
                input("Presione Enter para continuar...")
        except Exception as error:
            print(f"\nOcurrió un error inesperado en la navegación: {error}")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    try:
        crear_tablas()
        dao_check = UsuarioDAO("ecotech.db")
        if not dao_check.obtener_todos():
            poblar_base_datos()
    except Exception as error:
        print("Error al preparar la base de datos:", error)
    else:
        main()