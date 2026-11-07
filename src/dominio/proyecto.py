class Proyecto:
    ESTADOS_VALIDOS = ("pendiente", "en_progreso", "finalizado", "cancelado")

    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin=None,
                 estado="pendiente", id_proyecto=None):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = estado
        self._empleados = []
        self._registros_tiempo = []
        self.validar()

    def validar(self):
        if not self._nombre or not self._nombre.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío")
        if not self._descripcion or not self._descripcion.strip():
            raise ValueError("La descripción del proyecto no puede estar vacía")
        if self._fecha_fin and self._fecha_fin < self._fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio")
        if self._estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use: {self.ESTADOS_VALIDOS}")

    def actualizar_datos(self, nombre=None, descripcion=None):
        if nombre is not None:
            self._nombre = nombre
        if descripcion is not None:
            self._descripcion = descripcion
        self.validar()

    def actualizar_fechas(self, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio is not None:
            self._fecha_inicio = fecha_inicio
        if fecha_fin is not None:
            self._fecha_fin = fecha_fin
        self.validar()

    def cambiar_estado(self, estado: str):
        if estado not in self.ESTADOS_VALIDOS:
            return False
        self._estado = estado
        return True

    def asignar_empleado(self, empleado):
        if empleado is None or empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def desvincular_empleado(self, empleado):
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True

    def agregar_registro_tiempo(self, registro):
        if registro is None or registro._proyecto != self:
            return False
        if registro._empleado not in self._empleados:
            return False
        if registro._horas_trabajadas <= 0:
            return False
        if registro in self._registros_tiempo:
            return False
        self._registros_tiempo.append(registro)
        return True

    def generar_informe(self):
        total_horas = sum(r._horas_trabajadas for r in self._registros_tiempo)
        return (f"Proyecto: {self._nombre}\n"
                f"Inicio: {self._fecha_inicio} | Fin: {self._fecha_fin}\n"
                f"Estado: {self._estado}\n"
                f"Empleados: {len(self._empleados)}\n"
                f"Horas registradas: {total_horas}")

    def __str__(self):
        return f"Proyecto(id={self._id_proyecto}, nombre='{self._nombre}', estado='{self._estado}')"