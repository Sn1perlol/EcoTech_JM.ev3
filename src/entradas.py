def pedir_dato(mensaje, validador, leer=input):
    while True:
        try:
            entrada = leer(mensaje)
            resultado = validador(entrada)
            if resultado is None:
                print("Entrada no válida. Intenta nuevamente.")
                continue
            return resultado
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")
        except Exception as error:
            print(f"Error inesperado: {error}. Intenta nuevamente.")