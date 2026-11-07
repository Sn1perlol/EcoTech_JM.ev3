import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado
from persistencia.departamento_dao import DepartamentoDAO
from dominio.departamento import Departamento
from persistencia.usuario_dao import UsuarioDAO
from dominio.usuario import Usuario


def cargar_departamentos():
    # Nuevos departamentos
    departamento_ej = [
        (1, 'Innovación y Desarrollo', 1),
        (2, 'Recursos Humanos', 2),
        (3, 'Operaciones', 3),
        (4, 'Finanzas', 4),
        (5, 'Atención al Cliente', 5),
    ]
    for id_dept, nombre, id_gerente in departamento_ej:
        existente = DepartamentoDAO.buscar_por_id(id_dept)
        if existente is None:
            dept = Departamento(
                nombre,
                descripcion=f"Área encargada de {nombre.lower()}",
                gerente=EmpleadoDAO.buscar_por_id(id_gerente),
                id_departamento=id_dept,
            )
            DepartamentoDAO.insertar(dept)
            print(f"Creado departamento: {nombre}")
        else:
            print(f"Ya existe departamento: {nombre}")


def cargar_empleados(dept_demo):
    # Nuevos empleados con datos distintos
    empleados_ej = [
        (1, 'Alejandro Rivas', 'Av. Libertad 1420', '981112223', 'alejandro.rivas@ecotech.cl', '2023-03-12', 980000, 'Ingeniero de Datos'),
        (2, 'Sofía Valdés', 'Calle Los Aromos 87', '982223334', 'sofia.valdes@ecotech.cl', '2021-07-05', 1250000, 'Jefa de Tecnología'),
        (3, 'Diego Fuentes', 'Pasaje El Roble 45', '983334445', 'diego.fuentes@ecotech.cl', '2022-11-20', 870000, 'Analista de Operaciones'),
        (4, 'Valentina Castro', 'Av. Central 321', '984445556', 'valentina.castro@ecotech.cl', '2020-02-14', 1400000, 'Directora de Finanzas'),
        (5, 'Martín Herrera', 'Calle Los Cedros 210', '985556667', 'martin.herrera@ecotech.cl', '2023-06-30', 760000, 'Especialista en Clientes'),
        (6, 'Camila Ortiz', 'Av. del Mar 515', '986667778', 'camila.ortiz@ecotech.cl', '2022-04-08', 890000, 'Diseñadora UX'),
        (7, 'José Molina', 'Calle Los Pinos 99', '987778889', 'jose.molina@ecotech.cl', '2021-09-17', 1120000, 'Desarrollador Backend'),
        (8, 'Paula Jiménez', 'Av. Los Robles 780', '988889990', 'paula.jimenez@ecotech.cl', '2023-01-23', 950000, 'Coordinadora de RRHH'),
        (9, 'Andrés Paredes', 'Pasaje Los Olmos 12', '989990001', 'andres.paredes@ecotech.cl', '2020-05-19', 1320000, 'Gerente de Operaciones'),
        (10, 'Francisca Navarro', 'Av. del Sol 456', '981234567', 'francisca.navarro@ecotech.cl', '2024-02-11', 870000, 'Especialista en Marketing'),
    ]
    for id_emp, nombre, direccion, numero, correo, fecha, salario, cargo in empleados_ej:
        existente = EmpleadoDAO.buscar_por_id(id_emp)
        if existente is None:
            emp = Empleado(nombre, direccion, str(numero), correo, fecha, salario, cargo, id_emp)
            EmpleadoDAO.insertar(emp)
            print(f"Creado empleado: {nombre}")
        else:
            print(f"Ya existe empleado: {nombre}")


def crear_admin_inicial():
    dao_usuario = UsuarioDAO('ecotech.db')
    usuarios = dao_usuario.obtener_todos()
    admin_existente = next((u for u in usuarios if u.nombre_usuario == 'admin'), None)
    if admin_existente is not None:
        print("El usuario 'admin' ya existe en la base de datos.")
        return

    # Aseguramos que exista el empleado 3 (Sofía Valdés) para asociar el admin
    if EmpleadoDAO.buscar_por_id(3) is None:
        emp_admin = Empleado('Sofía Valdés', 'Calle Los Aromos 87', '982223334',
                             'sofia.valdes@ecotech.cl', '2021-07-05', 1250000.0,
                             'Jefa de Tecnología', 3)
        EmpleadoDAO.insertar(emp_admin)

    # Usuario admin nuevo: usuario "admin_eco", clave "eco2026"
    admin = Usuario(
        nombre_usuario='admin_eco',
        mail='admin_eco@ecotech.cl',
        contrasenia='eco2026',
        id_empleado=3
    )
    if 'administrar_permisos' not in admin._permisos:
        admin._permisos.append('administrar_permisos')
    dao_usuario.crear(admin)
    print("Usuario 'admin_eco' creado exitosamente con permiso 'administrar_permisos'.")


def cargar_proyectos():
    # Nuevos proyectos de ejemplo (requiere importar ProyectoDao)
    from persistencia.proyecto_dao import ProyectoDao
    from dominio.proyecto import Proyecto
    from datetime import date

    proyectos_ej = [
        (1, 'Plataforma Verde', 'Sistema de gestión de residuos para clientes corporativos',
         date(2024, 1, 15), None, 'en_progreso'),
        (2, 'Portal de Clientes', 'Nuevo portal de autogestión para clientes B2B',
         date(2024, 3, 1), date(2024, 12, 31), 'en_progreso'),
        (3, 'App EcoRuta', 'Aplicación móvil para monitoreo de rutas de reciclaje',
         date(2023, 8, 10), date(2024, 5, 30), 'finalizado'),
        (4, 'Migración Cloud', 'Traslado de servidores locales a la nube',
         date(2024, 6, 1), None, 'pendiente'),
    ]
    for id_p, nombre, desc, inicio, fin, estado in proyectos_ej:
        existente = ProyectoDao.buscar_por_id(id_p)
        if existente is None:
            proy = Proyecto(nombre, desc, inicio, fecha_fin=fin, estado=estado, id_proyecto=id_p)
            ProyectoDao.insertar(proy)
            print(f"Creado proyecto: {nombre}")
        else:
            print(f"Ya existe proyecto: {nombre}")


def poblar_base_datos():
    print("--- INICIANDO POBLAMIENTO DE BASE DE DATOS ---")
    cargar_departamentos()
    dept_demo = DepartamentoDAO.buscar_por_id(1)
    cargar_empleados(dept_demo)
    cargar_proyectos()
    crear_admin_inicial()
    print("--- BASE DE DATOS POBLADA CON ÉXITO ---")


if __name__ == "__main__":
    poblar_base_datos()