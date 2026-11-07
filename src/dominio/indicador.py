class Indicador:
    def __init__(self, fecha, valor, fuente="mindicador.cl"):
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"

    def __str__(self):
        return f"{self.fecha}: {self.valor:.2f} {self.unidad} (Fuente: {self.fuente})"