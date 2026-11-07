class Empleado:
    def __init__(self, nombre, direccion, numero, correo, fecha_contrato,
                 salario, cargo, id=None, departamento=None):
        self._id = id
        self._nombre = nombre
        self._direccion = direccion
        self._numero = numero
        self._correo = correo
        self._fecha_contrato = fecha_contrato
        self._salario = salario
        self._cargo = cargo
        self._departamento = departamento
        self._registros_tiempo = []
        self.validar()

    def validar(self):
        if not self._nombre or not self._nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not self._direccion or not self._direccion.strip():
            raise ValueError("La dirección no puede estar vacía")
        if not self._numero or not self._numero.strip():
            raise ValueError("El número telefónico no puede estar vacío")
        if "@" not in self._correo or "." not in self._correo:
            raise ValueError("El correo no es válido")
        if self._salario < 0:
            raise ValueError("El salario no puede ser negativo")
        if not self._cargo or not self._cargo.strip():
            raise ValueError("El cargo no puede estar vacío")

    def actualizar_datos(self, nombre=None, correo=None):
        if nombre is not None:
            self._nombre = nombre
        if correo is not None:
            self._correo = correo
        self.validar()

    def cambiar_departamento(self, departamento):
        if departamento is None:
            self._departamento = None
            return True
        from dominio.departamento import Departamento
        if not isinstance(departamento, Departamento):
            return False
        self._departamento = departamento
        return True

    def mostrar_datos(self):
        return f"{self._id} - {self._nombre} - {self._cargo} - {self._correo} - {self._direccion}"

    def ver_salario(self):
        return self._salario

    def registrar_horas(self, registro):
        if registro._empleado != self:
            raise ValueError("El registro pertenece a otro empleado")
        if registro._horas_trabajadas <= 0:
            raise ValueError("Las horas deben ser mayores que cero")
        if registro in self._registros_tiempo:
            raise ValueError("Este registro ya fue agregado")
        self._registros_tiempo.append(registro)
        return sum(r._horas_trabajadas for r in self._registros_tiempo)

    def __str__(self):
        return self.mostrar_datos()