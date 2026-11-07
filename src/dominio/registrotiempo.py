class RegistroTiempo:
    def __init__(self, empleado, proyecto, fecha, horas, descripcion, id_registro=None):
        self._id_registro = id_registro
        self._empleado = empleado
        self._proyecto = proyecto
        self._fecha_trabajada = fecha
        self._horas_trabajadas = horas
        self._descripcion_tarea = descripcion
        self.validar()

    def validar(self):
        if self._empleado is None:
            raise ValueError("El registro debe tener un empleado")
        if self._proyecto is None:
            raise ValueError("El registro debe tener un proyecto")
        if not isinstance(self._horas_trabajadas, (int, float)) or self._horas_trabajadas <= 0:
            raise ValueError("Las horas deben ser mayores que cero")
        if not self._descripcion_tarea or not self._descripcion_tarea.strip():
            raise ValueError("La descripción de la tarea no puede estar vacía")

    def actualizar_detalle(self, fecha=None, horas=None, descripcion=None):
        if fecha is not None:
            self._fecha_trabajada = fecha
        if horas is not None:
            self._horas_trabajadas = horas
        if descripcion is not None:
            self._descripcion_tarea = descripcion
        self.validar()

    def calculo_horas(self, registros):
        total = 0
        for r in registros:
            if r._empleado._id == self._empleado._id:
                total += r._horas_trabajadas
        return total

    def calculo_horas_proyecto(self, registros, proyecto):
        total = 0
        for r in registros:
            if (r._empleado._id == self._empleado._id
                    and r._proyecto._id_proyecto == proyecto._id_proyecto):
                total += r._horas_trabajadas
        return total

    def __str__(self):
        return (f"RegistroTiempo(id={self._id_registro}, empleado={self._empleado._nombre}, "
                f"proyecto={self._proyecto._nombre}, horas={self._horas_trabajadas})")