from complementos.complementos import limpiar_pantalla, validar_entero_positivo
from entradas import pedir_dato
from servicios.api import (
    obtener_datos, mostrar_indicador, convertir_clp_a_usd,
    obtener_pronostico_clima_3_dias, DATOS_RESPALDO,
)


def menu_api():
    while True:
        limpiar_pantalla()
        print("==================================================")
        print("         MÓDULO API - SERVICIOS Y CLIMA           ")
        print("==================================================")
        print("1. Valor actual del Dólar")
        print("2. Calculadora de Pago (CLP -> USD)")
        print("3. Pronóstico del Clima (3 días)")
        print("0. Volver")
        print("==================================================")
        opcion = input("\nOpción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return
        elif opcion == "1":
            try:
                datos, origen = obtener_datos()
                mostrar_indicador(datos, origen)
            except Exception:
                mostrar_indicador(DATOS_RESPALDO, "respaldo local")
            input("\nPresione Enter...")
        elif opcion == "2":
            try:
                monto = pedir_dato("Monto CLP: $",
                                   lambda v: validar_entero_positivo(v, "Monto"))
                usd, tasa, origen = convertir_clp_a_usd(float(monto))
                print(f"\nMonto: ${monto:,.0f} CLP")
                print(f"Tasa: ${tasa:.2f} CLP/USD")
                print(f"Origen: {origen}")
                print(f"Total: ${usd:,.2f} USD")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")
        elif opcion == "3":
            try:
                clima, fuente = obtener_pronostico_clima_3_dias()
                print(f"Fuente: {fuente}\n")
                print(f"{'Jornada':<15} | {'Mínima':<10} | {'Máxima':<10}")
                print("-" * 42)
                for c in clima:
                    mn = f"{c['temp_min']} °C" if c['temp_min'] != "N/A" else "N/A"
                    mx = f"{c['temp_max']} °C" if c['temp_max'] != "N/A" else "N/A"
                    print(f"{c['dia']:<15} | {mn:<10} | {mx:<10}")
            except Exception as error:
                print("Error:", error)
            input("\nPresione Enter...")
        else:
            print("Opción inválida.")
            input("\nPresione Enter...")