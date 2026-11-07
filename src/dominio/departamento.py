from dominio.empleado import Empleado
from dominio.proyecto import Proyecto


class Departamento:
    def __init__(self, nombre, descripcion="", gerente=None, id_departamento=None):
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._descripcion = descripcion
        self._gerente = gerente
        self._empleados = []
        self._proyectos = []
        self.validar()

    def validar(self):
        if not self._nombre or not self._nombre.strip():
            raise ValueError("El nombre del departamento no puede estar vacío")

    def actualizar_datos(self, nombre=None, correo=None):
        if nombre is not None:
            self._nombre = nombre
        self.validar()

    def asignar_gerente(self, gerente: Empleado):
        if gerente is not None and not isinstance(gerente, Empleado):
            return False
        self._gerente = gerente
        return True

    def contratar_empleado(self, empleado: Empleado, encargado: Empleado) -> bool:
        if empleado is None or encargado is None:
            return False
        if encargado._cargo != "Recursos Humanos":
            return False
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        empleado.cambiar_departamento(self)
        return True

    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado is None or empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        empleado.cambiar_departamento(self)
        return True

    def eliminar_empleado(self, empleado: Empleado) -> None:
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            empleado.cambiar_departamento(None)

    def crear_proyecto(self, proyecto: Proyecto) -> bool:
        if proyecto is None or proyecto in self._proyectos:
            return False
        self._proyectos.append(proyecto)
        return True

    def editar_proyecto(self, proyecto, nuevo_nombre: str) -> bool:
        if proyecto not in self._proyectos:
            return False
        if not nuevo_nombre or not nuevo_nombre.strip():
            return False
        proyecto._nombre = nuevo_nombre
        return True

    def eliminar_proyecto(self, proyecto) -> bool:
        if proyecto not in self._proyectos:
            return False
        self._proyectos.remove(proyecto)
        return True

    @property
    def empleados(self):
        return tuple(self._empleados)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    def __str__(self):
        return (f"Departamento(id={self._id_departamento}, nombre='{self._nombre}', "
                f"descripcion='{self._descripcion}')")